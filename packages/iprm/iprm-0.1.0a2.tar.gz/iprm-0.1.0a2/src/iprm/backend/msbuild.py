"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
from typing import cast
from iprm.util.loader import Loader
from iprm.backend.backend import BuildSystem, GenerateMode
from iprm.util.dir import Dir, CurrentSourceDir, CurrentBinaryDir, BinaryDir
from iprm.util.env import Env
from iprm.util.platform import PlatformContext, platform_context
from iprm.core.session import Session
from iprm.api.project import Project, SubDir
from iprm.api.target import Target
from iprm.api.cpp import CppTarget
from iprm.api.rust import RustTarget


class MSBuild(BuildSystem):
    _binary_dir_variable = 'IprmBinaryDir'

    _solution_file_ext = '.sln'
    _solution_folder_uuid = '2150E333-8FDC-42A3-9474-1A3956D46DE8'
    _solution_project_uuid = '8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942'

    _props_file_ext = '.props'

    _project_file_ext = '.vcxproj'
    _project_filter_file_ext = '.vcxproj.filters'

    _msbuild_x64_platform = 'x64'

    def __init__(self, native_loader: Loader, **kwargs):
        kwargs['build_dir'] = 'build'
        super().__init__(native_loader, **kwargs)
        self._native_loader = cast(Loader, self.loader)

    @classmethod
    def platforms(cls) -> list[PlatformContext]:
        # TODO: Wasm support will make all .vcxproj files custom builds
        return [Env.windows, Env.wasm]

    @classmethod
    def dir_separator(cls):
        return '\\'

    @classmethod
    def _generate_mode(cls):
        return GenerateMode.PER_OBJECT

    def _generate_file_name(self):
        return self._solution_file_ext if self._is_root_item else self._project_file_ext

    @classmethod
    def generate_file_exts(cls) -> list[str]:
        return [cls._solution_file_ext, cls._project_file_ext]

    def _add_generated_file_header(self) -> bool:
        return False

    def _generate_file_comment(self):
        return None

    def _generate_file_comment_prefix(self):
        return ''

    def _generate_file_comment_suffix(self):
        return ''

    @classmethod
    def _default_build_type(cls):
        return cls._release_build_type()

    @classmethod
    def _release_build_type(cls):
        return 'Release'

    @classmethod
    def _debug_build_type(cls):
        return 'Debug'

    @classmethod
    def _x64_platform_release_config(cls):
        return f'{cls._release_build_type()}|{cls._msbuild_x64_platform}'

    @classmethod
    def _x64_platform_debug_config(cls):
        return f'{cls._debug_build_type()}|{cls._msbuild_x64_platform}'

    @classmethod
    def build(cls, **kwargs):
        bindir = kwargs.get('bindir')
        target_path = kwargs.get('target', None)
        solution = kwargs.get('solution')
        cmd = [
            f'{solution}{cls._solution_file_ext}',
        ]
        if target_path:
            cmd.append(f'/t:{target_path}')

        cmd.extend([
            f'/p:{cls._binary_dir_variable}={bindir}',
            f'/p:Configuration={cls.build_type(**kwargs)}',
            f'/p:Platform={cls._msbuild_x64_platform}',
            f'/maxcpucount:{cls.num_procs(**kwargs)}',
        ])
        cmd.insert(0, 'msbuild')
        platform_ctx = kwargs.get('platform_ctx')
        return cls._run_command(cmd, platform_ctx)

    @classmethod
    def relative_src_path(cls, root_relative_path: Path, dir_path: Dir, leaf_path: str = None):
        leaf = '' if leaf_path is None else f'{cls.dir_separator()}{leaf_path}'
        prefix_dir = f'$(SolutionDir){str(root_relative_path)}'
        if isinstance(dir_path, CurrentSourceDir):
            return f'{prefix_dir}{leaf}'
        path = dir_path.path
        return f'{prefix_dir}{cls.dir_separator()}{path}{leaf}'

    @classmethod
    def current_bin_dir(cls):
        return f'$({cls._binary_dir_variable})'

    @classmethod
    def relative_bin_path(cls, root_relative_path: Path, dir_path: Dir, leaf_path: str = None):
        leaf = '' if leaf_path is None else f'{cls.dir_separator()}{leaf_path}'
        prefix_dir = f'$(SolutionDir){cls.current_bin_dir()}{cls.dir_separator()}{str(root_relative_path)}'
        if isinstance(dir_path, CurrentBinaryDir):
            return f'{prefix_dir}{leaf}'
        path = dir_path.path
        return f'{prefix_dir}{cls.dir_separator()}{path}{leaf}'

    def _generate_project(self, project: Project) -> list[str]:
        def _generate_project_entry(path: Path, uuid: str):
            path_name = path.name
            return (
                f'Project("{{{self._solution_folder_uuid}}}") = "{path_name}", "{path_name}", "{{{uuid}}}"\n'
                f'EndProject'
            )

        def _generate_nested_projects(fs: dict[Path, str]) -> list[str]:
            nested_mappings = []
            for child_path, child_uuid in fs.items():
                parent_path = child_path.parent
                if parent_path in fs:
                    parent_uuid = fs[parent_path]
                    nested_mappings.append(f'\t\t{{{child_uuid}}} = {{{parent_uuid}}}')
            return nested_mappings

        project_props_root_node = self._generate_global_props_xml(project)
        from lxml import etree
        project_props_tree = etree.ElementTree(project_props_root_node)

        project_props_path = project.parent_path / f"{project.name}{self._props_file_ext}"
        project_props_tree.write(project_props_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

        msbuild_content = [
            'Microsoft Visual Studio Solution File, Format Version 12.00',
        ]

        project_fs = {}
        project_section_content = []
        for subdir in self._native_loader.subdir_objects:
            path = subdir.path
            uuid = subdir.uuid
            project_section_content.append(_generate_project_entry(path, uuid))
            project_fs[path] = uuid

        project_config_platform_section_content = []
        for target in self._native_loader.target_objects:
            target_name = target.name
            target_uuid = target.uuid
            target_path = target.parent_path
            target_project_file = f'{target_name}{self._project_file_ext}'
            target_project_path = target_path.relative_to(
                self._native_loader.project_dir_abs_path) / target_project_file
            msbuild_content.extend([
                f'Project("{{{self._solution_project_uuid}}}") = "{target_name}", "{target_project_path}", "{{{target_uuid}}}"',
                f'EndProject'
            ])
            project_fs[target_path / target_project_file] = target_uuid
            project_config_platform_section_content.extend([
                f'\t\t{{{target_uuid}}}.{self._x64_platform_debug_config()}.ActiveCfg = {self._x64_platform_debug_config()}',
                f'\t\t{{{target_uuid}}}.{self._x64_platform_debug_config()}.Build.0 = {self._x64_platform_debug_config()}',
                f'\t\t{{{target_uuid}}}.{self._x64_platform_release_config()}.ActiveCfg = {self._x64_platform_release_config()}',
                f'\t\t{{{target_uuid}}}.{self._x64_platform_release_config()}.Build.0 = {self._x64_platform_release_config()}',
            ])

        msbuild_content.extend(project_section_content)

        msbuild_content.extend([
            'Global',
            '\tGlobalSection(SolutionConfigurationPlatforms) = preSolution',
            f'\t\t{self._x64_platform_debug_config()} = {self._x64_platform_debug_config()}',
            f'\t\t{self._x64_platform_release_config()} = {self._x64_platform_release_config()}',
            '\tEndGlobalSection',
        ])

        msbuild_content.append('\tGlobalSection(ProjectConfigurationPlatforms) = postSolution')
        msbuild_content.extend(project_config_platform_section_content)
        msbuild_content.append('\tEndGlobalSection')

        msbuild_content.extend([
            '\tGlobalSection(SolutionProperties) = preSolution',
            '\t\tHideSolutionNode = FALSE',
            '\tEndGlobalSection',
        ])

        msbuild_content.append('\tGlobalSection(NestedProjects) = preSolution')
        msbuild_content.extend(_generate_nested_projects(project_fs))
        msbuild_content.append('\tEndGlobalSection')

        msbuild_content.extend([
            '\tGlobalSection(ExtensibilityGlobals) = postSolution',
            f'\t\tSolutionGuid = {{{project.uuid}}}',
            '\tEndGlobalSection',
            'EndGlobal',
            '',
        ])
        return msbuild_content

    def _generate_subdir(self, subdir: SubDir) -> list[str]:
        pass

    def _generate_target(self, target: Target) -> list[str]:
        from lxml import etree
        target_vcxproj_filters_root_node = self._generate_vcxproj_filters_xml(target)
        target_vcxproj_filters_tree = etree.ElementTree(target_vcxproj_filters_root_node)
        target_filters_path = target.parent_path / f"{target.name}{self._project_filter_file_ext}"
        target_vcxproj_filters_tree.write(target_filters_path, encoding="utf-8", xml_declaration=True,
                                          pretty_print=True)

        target_vcxproj_root_node = self._generate_vcxproj_xml(target)
        target_vcxproj_tree = etree.ElementTree(target_vcxproj_root_node)
        return [etree.tostring(target_vcxproj_tree, encoding="utf-8", xml_declaration=True, pretty_print=True).decode(
            "utf-8")]

    def _generate_cpp(self, cpp: CppTarget):
        return self._generate_target(cpp)

    def _generate_rust(self, rust: RustTarget) -> list[str]:
        return self._generate_target(rust)

    def _generate_global_props_xml(self, project: Project):

        # TODO: Add helpers to reduce duplication for debug and release elements

        from lxml import etree
        nsmap = {None: "http://schemas.microsoft.com/developer/msbuild/2003"}
        root = etree.Element("Project", attrib={"DefaultTargets": "Build"}, nsmap=nsmap)

        debug_prop_group = etree.SubElement(root, "PropertyGroup",
                                            attrib={
                                                "Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_debug_config()}'"})

        debug_preprocessor_defines = ["_DEBUG", "WIN32", "_CONSOLE"]
        etree.SubElement(debug_prop_group, "PreprocessorDefinitions").text = f"{';'.join(debug_preprocessor_defines)}"

        release_prop_group = etree.SubElement(root, "PropertyGroup",
                                              attrib={
                                                  "Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_release_config()}'"})

        release_preprocessor_defines = ["NDEBUG", "WIN32", "_CONSOLE"]
        etree.SubElement(release_prop_group,
                         "PreprocessorDefinitions").text = f"{';'.join(release_preprocessor_defines)}"

        common_prop_group = etree.SubElement(root, "PropertyGroup")

        cpp_standards = {
            '14': 'stdcpp14',
            '17': 'stdcpp17',
            '20': 'stdcpp20',
            '23': 'stdcpp23',
            'latest': 'stdcpplatest',
        }

        langs_dict = project.properties.get('languages', {})
        cpp_lang_props = langs_dict.get(CppTarget.__name__, {})
        if cpp_lang_props:
            common_item_def_group = etree.SubElement(root, "ItemDefinitionGroup")
            cl_compile = etree.SubElement(common_item_def_group, "ClCompile")
            standard_value = cpp_standards.get(cpp_lang_props.get(CppTarget.STANDARD))
            etree.SubElement(cl_compile, "LanguageStandard").text = standard_value

            if cpp_lang_props.get(CppTarget.CONFORMANCE):
                additional_options = etree.SubElement(cl_compile, "ConformanceMode")
                additional_options.text = "true"
        return root

    def _generate_vcxproj_xml(self, target: Target):
        from lxml import etree
        nsmap = {None: "http://schemas.microsoft.com/developer/msbuild/2003"}
        root = etree.Element("Project", attrib={"DefaultTargets": "Build"}, nsmap=nsmap)

        header_comment = etree.Comment('\n'.join(self._generate_file_header()))
        root.insert(0, header_comment)

        config_item_group = etree.SubElement(root, "ItemGroup", attrib={"Label": "ProjectConfigurations"})

        debug_config = etree.SubElement(config_item_group, "ProjectConfiguration",
                                        attrib={"Include": self._x64_platform_debug_config()})
        etree.SubElement(debug_config, "Configuration").text = self._debug_build_type()
        etree.SubElement(debug_config, "Platform").text = self._msbuild_x64_platform

        release_config = etree.SubElement(config_item_group, "ProjectConfiguration",
                                          attrib={"Include": self._x64_platform_release_config()})
        etree.SubElement(release_config, "Configuration").text = self._release_build_type()
        etree.SubElement(release_config, "Platform").text = self._msbuild_x64_platform

        globals_prop_group = etree.SubElement(root, "PropertyGroup", attrib={"Label": "Globals"})
        etree.SubElement(globals_prop_group, "Keyword").text = "Win32Proj"
        etree.SubElement(globals_prop_group, "ProjectGuid").text = f"{{{target.uuid}}}"
        etree.SubElement(globals_prop_group, "RootNamespace").text = target.name
        etree.SubElement(globals_prop_group, "TargetName").text = target.name
        suffix = target.properties.get('suffix', '')
        if suffix:
            suffix = f'.{suffix}' if not suffix.startswith('.') else suffix
            etree.SubElement(globals_prop_group, "TargetExt").text = suffix
        # TODO: Allow this to be configurable, but for now just let MSBuild use the default
        # etree.SubElement(globals_prop_group, "WindowsTargetPlatformVersion").text = "10.0"

        target_config_type = ''
        if target.is_app or target.is_test:
            target_config_type = 'Application'
        elif target.is_header:
            target_config_type = 'Utility'
        elif target.is_static:
            target_config_type = 'StaticLibrary'
        elif target.is_shared or target.is_python:
            target_config_type = 'DynamicLibrary'

        etree.SubElement(root, "Import", attrib={"Project": "$(VCTargetsPath)\\Microsoft.Cpp.Default.props"})

        # TODO: Allow platform toolset to be specified for each target instead of hardcoding to vc143
        debug_prop_group = etree.SubElement(root, "PropertyGroup",
                                            attrib={
                                                "Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_debug_config()}'",
                                                "Label": "Configuration"})
        etree.SubElement(debug_prop_group, "ConfigurationType").text = target_config_type
        etree.SubElement(debug_prop_group, "UseDebugLibraries").text = "true"
        etree.SubElement(debug_prop_group, "PlatformToolset").text = "v143"
        etree.SubElement(debug_prop_group, "CharacterSet").text = "Unicode"

        release_prop_group = etree.SubElement(root, "PropertyGroup",
                                              attrib={"Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_release_config()}'",
                                                      "Label": "Configuration"})
        etree.SubElement(release_prop_group, "ConfigurationType").text = target_config_type
        etree.SubElement(release_prop_group, "UseDebugLibraries").text = "false"
        etree.SubElement(release_prop_group, "PlatformToolset").text = "v143"
        etree.SubElement(release_prop_group, "WholeProgramOptimization").text = "true"
        etree.SubElement(release_prop_group, "CharacterSet").text = "Unicode"

        etree.SubElement(root, "Import", attrib={"Project": "$(VCTargetsPath)\\Microsoft.Cpp.props"})
        etree.SubElement(root, "Import",
                         attrib={"Project": f"$(SolutionDir)\\{self._native_loader.project_object.name}.props"})
        etree.SubElement(root, "ImportGroup", attrib={"Label": "ExtensionSettings"})
        etree.SubElement(root, "ImportGroup", attrib={"Label": "ExtensionSettings"})

        prop_sheets_import_group = etree.SubElement(root, "ImportGroup",
                                                    attrib={"Label": "PropertySheets"})
        etree.SubElement(prop_sheets_import_group, "Import",
                         attrib={"Project": "$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props",
                                 "Condition": "exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')",
                                 "Label": "LocalAppDataPlatform"})

        etree.SubElement(root, "PropertyGroup", attrib={"Label": "UserMacros"})

        target_path = target.parent_path
        target_project_path = str(target_path.relative_to(self._native_loader.project_dir_abs_path))

        debug_prop_group_config = etree.SubElement(root, "PropertyGroup",
                                                   attrib={
                                                       "Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_debug_config()}'",
                                                       "Label": "Configuration"})
        debug_prop_group_config_binary_dir_default = etree.SubElement(debug_prop_group_config, f"{self._binary_dir_variable}",
                                                                attrib={"Condition": f"'{self.current_bin_dir()}' == ''"})


        debug_prop_group_config_binary_dir_default.text = 'build'
        etree.SubElement(debug_prop_group_config, "OutDir").text = f"$(SolutionDir){self.current_bin_dir()}\\{target_project_path}\\$(Platform)\\$(Configuration)\\"
        etree.SubElement(debug_prop_group_config, "IntDir").text = f"$(SolutionDir){self.current_bin_dir()}\\{target_project_path}\\$(Platform)\\$(Configuration)\\"

        release_prop_group_config = etree.SubElement(root, "PropertyGroup",
                                                     attrib={
                                                         "Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_release_config()}'",
                                                         "Label": "Configuration"})
        release_prop_group_config_binary_dir_default = etree.SubElement(release_prop_group_config, f"{self._binary_dir_variable}",
                                                                attrib={"Condition": f"'{self.current_bin_dir()}' == ''"})
        release_prop_group_config_binary_dir_default.text = 'build'
        etree.SubElement(release_prop_group_config, "OutDir").text = f"$(SolutionDir){self.current_bin_dir()}\\{target_project_path}\\$(Platform)\\$(Configuration)\\"
        etree.SubElement(release_prop_group_config, "IntDir").text = f"$(SolutionDir){self.current_bin_dir()}\\{target_project_path}\\$(Platform)\\$(Configuration)\\"

        include_paths = target.properties.get('include_paths', [])
        root_relative_path = target.root_relative_dir.path
        src_include_paths = [self.relative_src_path(root_relative_path, include_path) for include_path in include_paths if not include_path.binary]
        bin_include_paths = [self.relative_bin_path(root_relative_path, include_path) for include_path in include_paths if include_path.binary]

        extra_include_paths = []

        library_paths = []
        dll_library_paths = []
        libraries = []

        if isinstance(target, CppTarget):
            cpp = cast(CppTarget, target)
            dependencies = cpp.dependencies
            if dependencies:
                for dependency in dependencies:
                    with platform_context(Env.platform):
                        dependency_obj = Session.get_object(dependency)
                        if not dependency_obj:
                            continue
                        dependency_obj_include_paths = dependency_obj.properties.get('include_paths', [])
                        dependency_obj_root_relative_path = dependency_obj.root_relative_dir.path
                        src_include_paths += [self.relative_src_path(dependency_obj_root_relative_path, include_path) for include_path in dependency_obj_include_paths if not include_path.binary]
                        bin_include_paths += [self.relative_bin_path(dependency_obj_root_relative_path, include_path) for include_path in dependency_obj_include_paths if include_path.binary]

                        dependency_obj_bin_path = f'$(SolutionDir){self.current_bin_dir()}{self.dir_separator()}{str(dependency_obj.root_relative_dir.path)}{self.dir_separator()}$(Platform){self.dir_separator()}$(Configuration)'

                        if dependency_obj.is_third_party and dependency_obj.is_imported:
                            library_paths.append(dependency_obj_bin_path)
                            libraries.append(f"{dependency_obj.name}.lib")
                        if (target.is_app or target.is_test) and dependency_obj.is_shared:
                            dll_library_paths.append(f'{dependency_obj_bin_path}{self.dir_separator()}{dependency_obj.name}.dll')

        if target.is_python:
            python_env = self._find_python()
            if python_env['FOUND']:
                extra_include_paths.append(python_env['INCLUDE_DIR'])
                library_paths.append(python_env['LIBRARY_DIR'])
                libraries.append(f"{python_env['LIBRARY']}.lib")

        include_paths_text = ';'.join(list(set(src_include_paths + bin_include_paths + extra_include_paths)))
        library_paths_text = ';'.join(list(set(library_paths)))
        libraries_text = ';'.join(list(set(libraries)))

        custom_build_steps = []
        if target.is_third_party and target.is_git:
            tag = target.properties.get('git_tag')
            repository = target.properties.get('git_repository')
            clone_path = f'$(SolutionDir){self.current_bin_dir()}{self.dir_separator()}{str(target.properties.get('git_clone_dir').path)}'
            clone_marker = f'{clone_path}{self.dir_separator()}git_clone_complete.marker'
            custom_build_steps.append({
                'command': f'''
if not exist "{clone_marker}" (
    git clone --depth 1 --branch {tag} {repository} {clone_path}
    echo. > "{clone_marker}"
)
    ''',
                'message': f'Clone {target.name} git repository...',
                'output': clone_marker
            })

        debug_def_group = etree.SubElement(root, "ItemDefinitionGroup",
                                           attrib={"Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_debug_config()}'"})

        debug_compile = etree.SubElement(debug_def_group, "ClCompile")
        etree.SubElement(debug_compile,
                         "AdditionalIncludeDirectories").text = f"{include_paths_text};%(AdditionalIncludeDirectories)"


        debug_link = etree.SubElement(debug_def_group, "Link")
        etree.SubElement(debug_link,
                         "AdditionalLibraryDirectories").text = f"{library_paths_text};%(AdditionalLibraryDirectories)"
        etree.SubElement(debug_link,
                         "AdditionalDependencies").text = f"{libraries_text};%(AdditionalDependencies)"

        if target.is_app or target.is_test:
            sub_system = 'Console'
            if target.is_gui:
                sub_system = 'Windows'
            etree.SubElement(debug_link,"SubSystem").text = sub_system

        if suffix:
            etree.SubElement(debug_link,
                             "OutputFile").text = f'$(OutDir)$(TargetName){suffix}'

        for custom_build_step in custom_build_steps:
            custom_build_element = "CustomBuildStep" if target.is_header else "PreBuildEvent"
            debug_custom_build_step = etree.SubElement(debug_def_group, custom_build_element)
            command = custom_build_step['command']
            message = custom_build_step['message']
            output = custom_build_step['output']
            etree.SubElement(debug_custom_build_step, "Command").text = command
            etree.SubElement(debug_custom_build_step, "Message").text = message
            etree.SubElement(debug_custom_build_step, "Outputs").text = output
            etree.SubElement(debug_custom_build_step, "Inputs").text = '$(MSBuildProjectFile)'


        if dll_library_paths:
            debug_pre_build_command = etree.SubElement(debug_def_group, "PreBuildEvent")
            copy_commands = [f'copy "{path}" "$(OutDir)"' for path in dll_library_paths]
            etree.SubElement(debug_pre_build_command, "Command").text = ' &amp; \n    '.join(copy_commands)
            etree.SubElement(debug_pre_build_command, "Message").text = "Copying run time DLLs..."

        # NOTE: Debug builds don't automatically run the test executables as we want them to be debuggable in Visual
        # Studio if there is run time errors

        release_def_group = etree.SubElement(root, "ItemDefinitionGroup",
                                             attrib={"Condition": f"'$(Configuration)|$(Platform)'=='{self._x64_platform_release_config()}'"})

        release_compile = etree.SubElement(release_def_group, "ClCompile")
        etree.SubElement(release_compile,
                         "AdditionalIncludeDirectories").text = f"{include_paths_text};%(AdditionalIncludeDirectories)"


        release_link = etree.SubElement(release_def_group, "Link")
        etree.SubElement(release_link,
                         "AdditionalLibraryDirectories").text = f"{library_paths_text};%(AdditionalLibraryDirectories)"
        etree.SubElement(release_link,
                         "AdditionalDependencies").text = f"{libraries_text};%(AdditionalDependencies)"

        if target.is_app or target.is_test:
            sub_system = 'Console'
            if target.is_gui:
                sub_system = 'Windows'
            etree.SubElement(release_link,"SubSystem").text = sub_system

        if suffix:
            etree.SubElement(release_link,
                             "OutputFile").text = f'$(OutDir)$(TargetName){suffix}'

        for custom_build_step in custom_build_steps:
            custom_build_element = "CustomBuildStep" if target.is_header else "PreBuildEvent"
            release_custom_build_step = etree.SubElement(release_def_group, custom_build_element)
            command = custom_build_step['command']
            message = custom_build_step['message']
            output = custom_build_step['output']
            etree.SubElement(release_custom_build_step, "Command").text = command
            etree.SubElement(release_custom_build_step, "Message").text = message
            etree.SubElement(release_custom_build_step, "Outputs").text = output
            etree.SubElement(release_custom_build_step, "Inputs").text = '$(MSBuildProjectFile)'

        if dll_library_paths:
            release_pre_build_command = etree.SubElement(release_def_group, "PreBuildEvent")
            copy_commands = [f'copy "{path}" "$(OutDir)"' for path in dll_library_paths]
            etree.SubElement(release_pre_build_command, "Command").text = ' &amp; \n    '.join(copy_commands)
            etree.SubElement(release_pre_build_command, "Message").text = "Copying run time DLLs..."

        if target.is_test:
            release_post_build_command = etree.SubElement(release_def_group, "PostBuildEvent")
            etree.SubElement(release_post_build_command, "Command").text = '"$(TargetPath)"'

        if isinstance(target, CppTarget):
            cpp = cast(CppTarget, target)

            if cpp.compiler_supports_property(cpp.compiler_flag, 'microsoft_crt'):
                from iprm.api.cpp import MicrosoftCRuntime
                crt = cpp.properties.get('microsoft_crt', MicrosoftCRuntime.DYNAMIC)
                if crt == MicrosoftCRuntime.DYNAMIC:
                    etree.SubElement(debug_compile, "RuntimeLibrary").text = "MultiThreadedDebugDLL"
                    etree.SubElement(release_compile, "RuntimeLibrary").text = "MultiThreadedDLL"
                elif crt == MicrosoftCRuntime.STATIC:
                    etree.SubElement(debug_compile, "RuntimeLibrary").text = "MultiThreadedDebug"
                    etree.SubElement(release_compile, "RuntimeLibrary").text = "MultiThreaded"

            preprocessor_defines_test = ';'.join(cpp.properties.get('defines', []))
            etree.SubElement(debug_compile,
                             "PreprocessorDefinitions").text = f"{preprocessor_defines_test};%(PreprocessorDefinitions)"
            etree.SubElement(release_compile,
                             "PreprocessorDefinitions").text = f"{preprocessor_defines_test};%(PreprocessorDefinitions)"

            self._cpp_add_compile_items(cpp, root)
            dependencies = cpp.dependencies
            if dependencies:
                dependencies_item_group = etree.SubElement(root, "ItemGroup")
                for dependency in dependencies:
                    with platform_context(Env.platform):
                        dependency_obj = Session.get_object(dependency)
                        if not dependency_obj:
                            continue
                        project_reference = etree.SubElement(dependencies_item_group, "ProjectReference")
                        dependency_obj_name = dependency_obj.name
                        dependency_obj_path = dependency_obj.parent_path
                        dependency_obj_project_path = str(dependency_obj_path.relative_to(
                            self._native_loader.project_dir_abs_path) / f'{dependency_obj_name}{self._project_file_ext}')
                        project_reference.set("Include", f"$(SolutionDir){dependency_obj_project_path}")

                        # Create the Project element as a child of ProjectReference
                        project_element = etree.SubElement(project_reference, "Project")
                        project_element.text = f"{{{dependency_obj.uuid}}}"

                        if not dependency_obj.is_header and dependency_obj.is_python:
                            ref_output_asm = etree.SubElement(project_reference, "ReferenceOutputAssembly")
                            ref_output_asm.text = 'false'
                            link_lib_deps = etree.SubElement(project_reference, "LinkLibraryDependencies")
                            link_lib_deps.text = 'false'
                            use_lib_dep_inputs = etree.SubElement(project_reference, "UseLibraryDependencyInputs")
                            use_lib_dep_inputs.text = 'false'
        elif isinstance(target, RustTarget):
            # TODO: Add Rust support
            pass


        etree.SubElement(root, "Import", attrib={"Project": "$(VCTargetsPath)\\Microsoft.Cpp.targets"})
        etree.SubElement(root, "ImportGroup", attrib={"Label": "ExtensionTargets"})
        return root

    def _generate_vcxproj_filters_xml(self, target: Target):
        nsmap = {None: "http://schemas.microsoft.com/developer/msbuild/2003"}
        from lxml import etree
        import uuid
        root = etree.Element("Project", attrib={"ToolsVersion": "4.0"}, nsmap=nsmap)
        filters_group = etree.SubElement(root, "ItemGroup")

        src_filter = etree.SubElement(filters_group, "Filter", attrib={"Include": "Source Files"})
        etree.SubElement(src_filter, "UniqueIdentifier").text = f"{str(uuid.uuid4()).upper()}"

        header_filter = etree.SubElement(filters_group, "Filter", attrib={"Include": "Header Files"})
        etree.SubElement(header_filter, "UniqueIdentifier").text = f"{str(uuid.uuid4()).upper()}"

        resource_filter = etree.SubElement(filters_group, "Filter", attrib={"Include": "Resource Files"})
        etree.SubElement(resource_filter, "UniqueIdentifier").text = f"{str(uuid.uuid4()).upper()}"

        if isinstance(target, CppTarget):
            cpp = cast(CppTarget, target)
            self._cpp_add_compile_items(cpp, root, add_filters=True)

        return root

    def _cpp_add_compile_items(self, cpp: CppTarget, root, add_filters=False):
        from lxml import etree
        source_files = self._cpp_get_source_src_file_paths(cpp)
        if source_files:
            source_item_group = etree.SubElement(root, "ItemGroup")
            for src in source_files:
                source_elem = etree.SubElement(source_item_group, "ClCompile", attrib={"Include": src})
                if add_filters:
                    etree.SubElement(source_elem, "Filter").text = 'Source Files'

        header_files = self._cpp_get_header_src_file_paths(cpp)
        if header_files:
            header_item_group = etree.SubElement(root, "ItemGroup")
            for header in header_files:
                header_elem = etree.SubElement(header_item_group, "ClInclude", attrib={"Include": header})
                if add_filters:
                    etree.SubElement(header_elem, "Filter").text = 'Header Files'

        resource_files = self._cpp_get_resource_src_file_paths(cpp)
        if resource_files:
            resource_item_group = etree.SubElement(root, "ItemGroup")
            for resource in resource_files:
                res_elem = None
                if resource.endswith(".rc"):
                    res_elem = etree.SubElement(resource_item_group, "ResourceCompile", attrib={"Include": resource})
                elif resource.endswith(".ico") or resource.endswith(".bmp"):
                    res_elem = etree.SubElement(resource_item_group, "Image", attrib={"Include": resource})
                else:
                    res_elem = etree.SubElement(resource_item_group, "None", attrib={"Include": resource})
                if add_filters and res_elem:
                    etree.SubElement(res_elem, "Filter").text = 'Resource Files'

    @staticmethod
    def _find_python(version=None):
        import sys, subprocess, os
        result = {
            'FOUND': False,
            'INCLUDE_DIR': None,
            'LIBRARY_DIR': None,
            'LIBRARY': None,
            'VERSION': None,
            'EXECUTABLE': None,
            'FRAMEWORK_PATH': None,
            'LINKFLAGS': []
        }

        result['EXECUTABLE'] = sys.executable
        result['VERSION'] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        if version and not version.startswith(f"{sys.version_info.major}.{sys.version_info.minor}"):
            print(f"Warning: Requested Python version {version} but found {result['VERSION']}")

        py_cmd = [
            sys.executable,
            "-c",
            "import sysconfig; print(sysconfig.get_path('include'))"
        ]
        result['INCLUDE_DIR'] = subprocess.check_output(py_cmd).decode().strip()

        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        if in_venv:
            py_cmd = [
                sys.executable,
                "-c",
                "import sys, os; " +
                "base_prefix = getattr(sys, 'real_prefix', getattr(sys, 'base_prefix', sys.prefix)); " +
                "print(os.path.join(base_prefix, 'libs'))"
            ]
        else:
            py_cmd = [
                sys.executable,
                "-c",
                "import sys, os; print(os.path.join(os.path.dirname(sys.executable), 'libs'))"
            ]
        result['LIBRARY_DIR'] = subprocess.check_output(py_cmd).decode().strip()
        result['LIBRARY'] = f"python{sys.version_info.major}{sys.version_info.minor}"

        lib_file = os.path.join(result['LIBRARY_DIR'], f"{result['LIBRARY']}.lib")
        if os.path.exists(lib_file):
            result['FOUND'] = True
        else:
            print(f"Warning: Python library {lib_file} not found.")
        return result
