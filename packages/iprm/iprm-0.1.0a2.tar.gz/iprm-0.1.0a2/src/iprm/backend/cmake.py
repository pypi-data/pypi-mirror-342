"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from itertools import zip_longest
from typing import Optional
from pathlib import Path
from iprm.core.session import Session
from iprm.util.env import Env
from iprm.util.dir import Dir, CurrentSourceDir, RootRelativeSourceDir, CurrentBinaryDir, RootRelativeBinaryDir
from iprm.util.platform import platform_context
from iprm.util.wasm import run_html_wasm_script
from iprm.backend.backend import ProjectModel
from iprm.util.loader import Loader
from iprm.api.project import Project, SubDir
from iprm.api.target import Target
from iprm.api.cpp import CppTarget
from iprm.api.rust import RustTarget


class CMake(ProjectModel):
    _cmake_file: str = 'CMakeLists.txt'
    _cmake_modules_dir: Optional[Path] = None
    _cmake_copy_runtime_dlls_module_file: Optional[Path] = None
    _cmake_qt_utils_module_file: Optional[Path] = None

    def __init__(self, native_loader: Loader, **kwargs):
        kwargs['build_dir'] = 'build'
        super().__init__(native_loader, **kwargs)
        CMake._cmake_modules_dir = Path(self.project_dir_str) / 'cmake'
        CMake._cmake_copy_runtime_dlls_module_file = CMake._cmake_modules_dir / 'copy_runtime_dlls.cmake'
        CMake._cmake_qt_utils_module_file = CMake._cmake_modules_dir / 'qt_utils.cmake'

    @classmethod
    def generator_ninja(cls):
        return 'Ninja'

    @classmethod
    def generator_xcode(cls):
        return 'Xcode'

    @classmethod
    def generator_visual_studio(cls):
        return '"Visual Studio 17 2022"'

    @classmethod
    def generator_unix_makefile(cls):
        return '"Unix Makefiles"'

    def _generate_file_name(self):
        return self._cmake_file

    @classmethod
    def generate_file_exts(cls) -> list[str]:
        return [cls._cmake_file]

    def _order_key(self, obj):
        pass

    @classmethod
    def supports_posix_paths(cls):
        return True

    @classmethod
    def current_src_dir(cls):
        return '${CMAKE_CURRENT_SOURCE_DIR}'

    @classmethod
    def src_dir(cls):
        return '${CMAKE_SOURCE_DIR}'

    # TODO: Consolidate the relative_*_path methods to share most of their code

    @classmethod
    def relative_src_path(cls, dir_path: Dir, leaf_path: str = None):
        leaf = '' if leaf_path is None else f'{cls.dir_separator()}{leaf_path}'
        prefix_dir = cls.current_src_dir()
        if isinstance(dir_path, CurrentSourceDir):
            return f'"{prefix_dir}{leaf}"'
        elif isinstance(dir_path, RootRelativeSourceDir):
            prefix_dir = cls.src_dir()
        path = dir_path.path
        return f'"{prefix_dir}{cls.dir_separator()}{path.as_posix() if cls.supports_posix_paths() else path}{leaf}"'

    @classmethod
    def current_bin_dir(cls):
        return '${CMAKE_CURRENT_BINARY_DIR}'

    @classmethod
    def bin_dir(cls):
        return '${CMAKE_BINARY_DIR}'

    @classmethod
    def relative_bin_path(cls, dir_path: Dir, leaf_path: str = None):
        leaf = '' if leaf_path is None else f'{cls.dir_separator()}{leaf_path}'
        prefix_dir = cls.current_bin_dir()
        if isinstance(dir_path, CurrentBinaryDir):
            return f'"{prefix_dir}{leaf}"'
        elif isinstance(dir_path, RootRelativeBinaryDir):
            prefix_dir = cls.bin_dir()
        path = dir_path.path
        return f'"{prefix_dir}{cls.dir_separator()}{path.as_posix() if cls.supports_posix_paths() else path}{leaf}"'

    @classmethod
    def _default_build_type(cls):
        cls._release_build_type()

    @classmethod
    def _release_build_type(cls):
        return 'Release'

    @classmethod
    def _debug_build_type(cls):
        return 'Debug'

    @classmethod
    def configure(cls, **kwargs):
        generator = kwargs.get('generator')
        srcdir = kwargs.get('srcdir')
        bindir = kwargs.get('bindir')
        cmd = [
            'cmake',
            '--fresh',
            '-G',
            generator,
            '-S',
            srcdir,
            '-B',
            bindir,
            f'-DCMAKE_BUILD_TYPE={cls.build_type(**kwargs)}',
        ]
        platform_ctx = kwargs.get('platform_ctx')
        if platform_ctx.wasm:
            cmd.insert(0, 'emcmake')
        return cls._run_command(cmd, platform_ctx)

    @classmethod
    def build(cls, **kwargs):
        bindir = kwargs.get('bindir')
        target = kwargs.get('target', None)
        cmd = [
            'cmake',
            '--build',
            bindir,
            '--config',
            cls.build_type(**kwargs),
            '--parallel',
            cls.num_procs(**kwargs),
        ]
        if target:
            cmd.extend(['--target', target])
        platform_ctx = kwargs.get('platform_ctx')
        return cls._run_command(cmd, platform_ctx)

    @classmethod
    def test(cls, **kwargs):
        bindir = kwargs.get('bindir')
        cmd = [
            'ctest',
            '--test-dir',
            bindir,
            '-C',
            cls.build_type(**kwargs),
        ]
        return cls._run_command(cmd)

    @classmethod
    def install(cls, **kwargs):
        # TODO: impl install
        pass

    def _generate_project(self, project: Project):
        # TODO: Don't hardcode minimum version, have it as a general config
        #  setting users can put on Object's, useful for scenarios like this where
        #  there is a generator-specific bit of data that is not generalizable to others
        cmake_content = [
            'cmake_minimum_required(VERSION 3.25)',
            '',
            f'project({project.name}',
            '\tVERSION',
            f'\t\t{project.properties.get('version', '0.1.0')}',
        ]
        description = project.properties.get('description', None)
        if description:
            cmake_content.append('\tDESCRIPTION')
            cmake_content.append(f'\t\t"{description}"')
        url = project.properties.get('url', None)
        if url:
            cmake_content.append('\tHOMEPAGE_URL')
            cmake_content.append(f'\t\t"{url}"')

        langs_dict = project.properties.get('languages', {})
        cmake_content_lang = []
        if langs_dict:
            cmake_content.append('\tLANGUAGES')
            langs_list = list(langs_dict.items())
            for (lang_type, lang_props), next_lang in zip_longest(langs_list, langs_list[1:], fillvalue=None):
                suffix = '' if next_lang is None else '\n'
                if lang_type == CppTarget.__name__:
                    cmake_content.append(f'\t\tCXX{suffix}')
                    standard = lang_props.get(CppTarget.STANDARD, None)
                    # TODO: Allow for project to specify full path to a compiler
                    """
                    compiler_flag = project.cpp_compiler_flag()
                    wasm_emscripten = compiler_flag == EMSCRIPTEN
                    windows_msvc = compiler_flag == MSVC
                    if not wasm_emscripten and not windows_msvc:
                        cmake_content_lang.append(f'set(CMAKE_CXX_COMPILER {project.cpp_compiler_binary()})')
                    """
                    if standard:
                        cmake_content_lang.append(f'set(CMAKE_CXX_STANDARD {standard})')
                        cmake_content_lang.append('set(CMAKE_CXX_STANDARD_REQUIRED True)')
                        cmake_content_lang.append('')
                    conformance = lang_props.get(CppTarget.CONFORMANCE, None)
                    if conformance:
                        cmake_content_lang.append('if(MSVC)')
                        cmake_content_lang.append('\tadd_compile_options(/Zc:__cplusplus /permissive-)')
                        cmake_content_lang.append('endif()')
                        cmake_content_lang.append('')

                elif lang_type == RustTarget.__name__:
                    # TODO: CMake does not yet support rust natively
                    # cmake_content.append(f'\t\tRUST{suffix}')
                    # cmake_content.append(f'set(CMAKE_RUST_COMPILER {project.rust_compiler_binary()})')
                    pass

        cmake_content.append(f')')
        cmake_content.append('')

        if cmake_content_lang:
            cmake_content.extend(cmake_content_lang)

        cmake_content.append('enable_testing()')
        cmake_content.append('')

        cmake_content.append('set_property(GLOBAL PROPERTY USE_FOLDERS ON)')
        cmake_content.append('')

        self._cmake_modules_dir.mkdir(exist_ok=True)
        if Env.platform.windows:
            if not self._cmake_copy_runtime_dlls_module_file.parent.exists():
                self._cmake_copy_runtime_dlls_module_file.parent.mkdir(parents=True)
            self._cmake_copy_runtime_dlls_module_file.write_text(f"""{self._current_generated_file_header}
if(DLL_FILES)
    execute_process(
        COMMAND ${{CMAKE_COMMAND}} -E copy_if_different ${{DLL_FILES}} "${{DEST_DIR}}"
    )
endif()
""")
        cmake_content.append('list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")')

        options = project.properties.get('options', {})
        if options:
            cmake_content.append('')
            for opt_name, opt_config in options.items():
                opt_description = opt_config.get('description')
                cmake_content.append(f'option({opt_name} "{opt_description}" ')
                opt_default = opt_config.get('default')
                opt_type = opt_config.get('type')
                if opt_type == bool:
                    cmake_content[-1] += 'ON' if opt_default else 'OFF'
                elif opt_type == int:
                    cmake_content[-1] += str(opt_default)
                elif opt_type == str:
                    cmake_content[-1] += f'"{opt_default}"'
                cmake_content[-1] += ')'
            cmake_content.append('')
        return cmake_content

    def _generate_subdir(self, subdir: SubDir):
        cmake_content = []
        dir_name = subdir.properties.get('dir_name', [])
        if dir_name:
            cmake_content.append(f'add_subdirectory({dir_name})')
        return cmake_content

    def _generate_target(self, target: Target):
        cmake_content = [
            'file(RELATIVE_PATH target_hierarchy ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})',
            f'set_target_properties({target.name}',
            '\tPROPERTIES',
            '\t\tFOLDER "${target_hierarchy}"',
        ]
        suffix = target.properties.get('suffix', None)
        if suffix:
            cmake_content.extend([
                f'\t\tSUFFIX "{suffix}"',
            ])
        cmake_content.append(')')
        return cmake_content

    def _generate_cpp(self, cpp: CppTarget):
        first_party = not cpp.is_third_party
        if first_party:
            return self._generate_cpp_first_party(cpp)
        else:
            return self._generate_cpp_third_party(cpp)

    def _generate_cpp_first_party(self, cpp: CppTarget):
        cmake_content = []
        target = cpp.name
        if cpp.is_app or cpp.is_test:
            cmake_content.append(f'add_executable({target})')
        elif cpp.is_static:
            cmake_content.append(f'add_library({target} STATIC)')
        elif cpp.is_shared:
            cmake_content.append(f'add_library({target} SHARED)')
        elif cpp.is_python:
            cmake_content.extend(self._generate_cpp_first_party_python_module(cpp))
        else:
            # If we didn't recognize/support the type, don't generate any content
            return cmake_content
        if cpp.is_test:
            # NOTE: Invoke `ctest --verbose` if we want the original
            # test executable output to be forwarding to output as well,
            # otherwise you'll only see the output if it fails (which is
            # the ideal default)
            cmake_content.append(f'add_test(NAME {target} COMMAND {target} --output-on-failure)')

        # TODO: For patches, create a custom command/target that applies the patches first before building,
        #  can just have this be a PRE_BUILD command instead of a custom target wrapper that the main target has to
        #  depend on
        # patches_dict = cpp.properties.get('patches', {})

        cmake_content.extend(self._cpp_add_sources(cpp, 'headers'))
        cmake_content.extend(self._cpp_add_sources(cpp, 'sources'))

        # TODO: each set for these properties (defines, include_paths, dependencies) will either be transitive or not,
        #  but for now just hardcode to always transitive for include_paths and dependencies and non-transitive for
        #  defines
        defines = cpp.properties.get('defines')
        if defines:
            cmake_content.append(f'target_compile_definitions({target}')
            cmake_content.append('\tPRIVATE')
            for define in defines:
                cmake_content.append(f'\t\t"{define}"')
            cmake_content.append(')')

        include_paths = cpp.properties.get('include_paths')
        if include_paths:
            cmake_content.append(f'target_include_directories({target}')
            cmake_content.append('\tPUBLIC')
            for include_path in include_paths:
                cmake_content.append(f'\t\t{self.relative_src_path(include_path)}')
            cmake_content.append(')')

        dependencies = cpp.dependencies
        py_module_dependencies = []
        if dependencies:
            cmake_content.append(f'target_link_libraries({target}')
            cmake_content.append('\tPUBLIC')
            for dependency in dependencies:
                with platform_context(Env.platform):
                    dependency_obj = Session.get_object(dependency)
                    if not dependency_obj:
                        continue
                    # CMake errors if we try to link directly with python modules as they are not STATIC or SHARED
                    # libraries
                    if dependency_obj.is_python and not dependency_obj.is_third_party:
                        py_module_dependencies.append(dependency_obj.name)
                    else:
                        cmake_content.append(f'\t\t{dependency}')
            cmake_content.append(')')

        if py_module_dependencies:
            cmake_content.append(f'add_dependencies({target}')
            for dependency in py_module_dependencies:
                cmake_content.append(f'\t{dependency}')
            cmake_content.append(')')

        cmake_content.extend(self._cpp_add_ms_crt(cpp))

        if cpp.is_qt:
            cmake_content.extend(self._cpp_qt_generate_sources(cpp))
        if cpp.is_python:
            cmake_content.append('find_package(Python COMPONENTS Interpreter Development REQUIRED)')
            cmake_content.append(f'target_link_libraries({target}')
            cmake_content.append('\tPRIVATE')
            cmake_content.append('\t\tPython::Python')
            cmake_content.append(')')

        if Env.platform.windows and cpp.is_app and cpp.is_gui:
            cmake_content.append(f'target_link_options({target}')
            cmake_content.append('\tPRIVATE')
            cmake_content.append('\t\t"/SUBSYSTEM:WINDOWS"')
            cmake_content.append('\t\t"/ENTRY:mainCRTStartup"')
            cmake_content.append(')')

        if Env.platform.wasm:
            cmake_content.append(f'target_link_options({target}')
            cmake_content.append('\tPRIVATE')
            cmake_content.append('\t\t"-s" "MINIFY_HTML=0"')
            cmake_content.append(')')

        if cpp.is_app or cpp.is_test:
            if Env.platform.windows:
                # TODO: Meson has a much cleaner way where we can just define the run target with an environment context
                #  that pre-pends on the shared lib/DLL directories to the PATH for this command. For now we'll take
                #  the inefficient approach here and just copy the DLLs, but we should fix/optimize this for CMake
                cmake_content.append(f'add_custom_command(TARGET {target} POST_BUILD')
                cmake_content.append('\tCOMMAND ${CMAKE_COMMAND}')
                cmake_content.append(f'\t"-DDLL_FILES=$<TARGET_RUNTIME_DLLS:{target}>"')
                cmake_content.append(f'\t"-DDEST_DIR=$<TARGET_FILE_DIR:{target}>"')
                cmake_content.append('\t"-P ${CMAKE_SOURCE_DIR}/cmake/copy_runtime_dlls.cmake"')
                cmake_content.append('\tVERBATIM')
                cmake_content.append(')')

            runtime_files = self._cpp_runtime_files(cpp)
            cmake_content.append(f'add_custom_command(TARGET {target} POST_BUILD')
            for runtime_file in runtime_files:
                cmake_content.append('\tCOMMAND ${CMAKE_COMMAND} -E copy_if_different')
                cmake_content.append(f'\t{runtime_file}')
                cmake_content.append(f'\t$<TARGET_FILE_DIR:{target}>')
            cmake_content.append('\tVERBATIM')
            cmake_content.append(')')

            runtime_paths = self._cpp_runtime_paths(cpp)
            cmake_content.append(f'add_custom_command(TARGET {target} POST_BUILD')
            for runtime_path in runtime_paths:
                cmake_content.append('\tCOMMAND ${CMAKE_COMMAND} -E copy_directory_if_different')
                cmake_content.append(f'\t{runtime_path}')
                cmake_content.append(f'\t$<TARGET_FILE_DIR:{target}>')
            cmake_content.append('\tVERBATIM')
            cmake_content.append(')')

            run_target = f'run_{target}'
            if Env.platform.wasm:
                suffix = cpp.properties.get('suffix', None)
                if suffix == '.html':
                    cmake_content.append('find_package(Python REQUIRED)')
                    run_target_script = f'"{self.current_bin_dir()}/{run_target}.py"'
                    cmake_content.append(f'file(WRITE {run_target_script} [[')
                    cmake_content.append(f'{run_html_wasm_script(target)}')
                    cmake_content.append(']])')
                    cmake_content.append(f'add_custom_target({run_target}')
                    port = cpp.properties.get('server_port', 8080)
                    cmake_content.append(
                        f'\tCOMMAND ${{Python_EXECUTABLE}} {run_target_script} "$<TARGET_FILE_NAME:{target}>" --port {port}')
                else:
                    # TODO: If suffix is .js, execute the file with Node.js
                    pass
            else:
                cmake_content.append(f'add_custom_target({run_target}')
                cmake_content.append(f'\t"$<TARGET_FILE_NAME:{target}>"')
            cmake_content.append(f'\tDEPENDS {target}')
            cmake_content.append(f'\tWORKING_DIRECTORY "$<TARGET_FILE_DIR:{target}>"')
            cmake_content.append(')')

        # TODO: Support output to custom bin dir not just src dir. Also, use actual target type to determine which
        #  properties to set instead of setting all of them
        output_dir = cpp.properties.get('output_dir', None)
        if output_dir:
            cmake_content.extend([
                f'set_target_properties({target}',
                '\tPROPERTIES',
            ])
            output_dir = self.relative_src_path(output_dir)
            cmake_content.extend([
                f'\t\tRUNTIME_OUTPUT_DIRECTORY {output_dir}',
                f'\t\tLIBRARY_OUTPUT_DIRECTORY {output_dir}',
                f'\t\tARCHIVE_OUTPUT_DIRECTORY {output_dir}',
            ])
            cmake_content.append(')')
        cmake_content.extend(self._generate_target(cpp))
        cmake_content.append('')
        return cmake_content

    def _generate_cpp_first_party_python_module(self, cpp: CppTarget):
        cmake_content = []
        target = cpp.name
        version_maj = cpp.properties.get('python_version_major')
        version_min = cpp.properties.get('python_version_minor')
        module_lib = cpp.properties.get('python_module_library')
        with platform_context(Env.platform):
            module_lib_target = Session.get_object(module_lib)
            # TODO: Support all ways to depend on pybind11 from the supported content sources, not just git
            # TODO: Remove hardcoded type name check via exposing the generator plugin API for plugin objects to
            #  generate specific content for given backends
            if type(module_lib_target).__name__ == 'PyBind11ThirdParty' and module_lib_target.is_git:
                cmake_content.append(f'set(PYBIND11_PYTHON_VERSION {version_maj}.{version_min})')
                cmake_content.append(f'pybind11_add_module({target})')
            else:
                # TODO: Add support for other known/popular C++ python module creation libraries
                pass
        return cmake_content

    def _generate_cpp_third_party(self, cpp: CppTarget):
        cmake_content = []
        if cpp.is_imported:
            cmake_content.extend(self._generate_cpp_third_party_imported(cpp))
        elif cpp.is_source_archive:
            cmake_content.extend(self._generate_cpp_third_party_source_archive(cpp))
        elif cpp.is_precompiled_archive:
            cmake_content.extend(self._generate_cpp_third_party_precompiled_archive(cpp))
        elif cpp.is_git:
            cmake_content.extend(self._generate_cpp_third_party_git(cpp))
        elif cpp.is_homebrew:
            cmake_content.extend(self._generate_cpp_third_party_homebrew(cpp))
        elif cpp.is_pkgconfig:
            cmake_content.extend(self._generate_cpp_third_party_pkgconfig(cpp))
        elif cpp.is_system:
            cmake_content.extend(self._generate_cpp_third_party_system(cpp))
        return cmake_content

    def _generate_cpp_third_party_source_archive(self, cpp: CppTarget):
        cmake_content = self._add_archive_unpack_variables(cpp)
        header_files = self._cpp_get_header_bin_file_paths(cpp)
        source_files = self._cpp_get_source_bin_file_paths(cpp)
        for header_file in header_files:
            cmake_content.append(f'list(APPEND archive_output_files {header_file})')
        for source_file in source_files:
            cmake_content.append(f'list(APPEND archive_output_files {source_file})')
        cmake_content.extend(self._add_archive_unpack_command(cpp))
        target = cpp.name
        build_target = target
        target_objects = f'{target}_objects'
        unpack_target_name = cpp.properties.get('unpack_target_name')
        if cpp.is_header:
            cmake_content.append(f'add_library({target} INTERFACE)')
            cmake_content.append(f'add_dependencies({target} {unpack_target_name})')
        else:
            build_target = target_objects
            cmake_content.append(f'add_library({target_objects} OBJECT)')
            cmake_content.append(f'target_sources({target_objects} PRIVATE ${{archive_output_files}})')
            cmake_content.append(f'set_source_files_properties(${{archive_output_files}}')
            cmake_content.append('\tPROPERTIES')
            cmake_content.append('\t\tGENERATED TRUE')
            cmake_content.append(')')
            cmake_content.append(f'add_dependencies({target_objects} {unpack_target_name})')

        include_paths = cpp.properties.get('include_paths')
        if include_paths:
            cmake_content.append(f'target_include_directories({build_target}')
            cmake_content.append(f'\t{"INTERFACE" if cpp.is_header else "PUBLIC"}')
            for include_path in include_paths:
                cmake_content.append(f'\t\t{self.relative_bin_path(include_path)}')
            cmake_content.append(')')

        dependencies = cpp.dependencies
        if dependencies:
            cmake_content.append(f'target_link_libraries({build_target}')
            cmake_content.append('\tPUBLIC')
            for dependency in dependencies:
                cmake_content.append(f'\t\t{dependency}')
            cmake_content.append(')')
        if cpp.is_qt:
            cmake_content.extend(self._cpp_qt_generate_sources(cpp, build_target))
        cmake_content.append('')
        if cpp.is_app or cpp.is_test:
            cmake_content.append(f'add_executable({target})')
        elif cpp.is_static:
            cmake_content.append(f'add_library({target} STATIC)')
        elif cpp.is_shared:
            cmake_content.append(f'add_library({target} SHARED)')
        else:
            return cmake_content
        cmake_content.append(f'target_sources({target} PRIVATE "$<TARGET_OBJECTS:{build_target}>")')
        if include_paths:
            cmake_content.append(f'target_include_directories({target}')
            cmake_content.append(f'\tPUBLIC')
            for include_path in include_paths:
                cmake_content.append(f'\t\t{self.relative_bin_path(include_path)}')
            cmake_content.append(')')
        cmake_content.extend(self._cpp_add_ms_crt(cpp))
        cmake_content.append(f'add_dependencies({target} {target_objects})')
        cmake_content.append('')
        return cmake_content

    def _generate_cpp_third_party_precompiled_archive(self, cpp: CppTarget):
        cmake_content = self._add_archive_unpack_variables(cpp)
        artifacts = cpp.properties.get('unpack_artifacts')
        archive_output_files = []
        for artifact in artifacts:
            lib_dir = artifact.get('lib_dir', None)
            if lib_dir:
                location_release, location_debug = self._extract_precompiled_lib_artifact(artifact)
                archive_output_files.append(self.relative_bin_path(lib_dir, location_release))
                if location_debug:
                    archive_output_files.append(self.relative_bin_path(lib_dir, location_debug))
            implib_dir = artifact.get('implib_dir', None)
            if implib_dir:
                implib_release, implib_debug = self._extract_precompiled_implib_artifact(artifact)
                archive_output_files.append(self.relative_bin_path(implib_dir, implib_release))
                if implib_debug:
                    archive_output_files.append(self.relative_bin_path(implib_dir, implib_debug))
            bin_dir = artifact.get('bin_dir', None)
            if bin_dir:
                location = self._extract_precompiled_bin_artifact(artifact)
                archive_output_files.append(self.relative_bin_path(bin_dir, location))

        archive_output_files = list(set(archive_output_files))
        for output_file in archive_output_files:
            cmake_content.append(f'list(APPEND archive_output_files {output_file})')
        cmake_content.extend(self._add_archive_unpack_command(cpp))

        target = cpp.name
        cmake_content.append(f'add_library({target} INTERFACE)')
        dependencies = cpp.dependencies
        if dependencies:
            cmake_content.append(f'target_link_libraries({target}')
            cmake_content.append('\tINTERFACE')
            for dependency in dependencies:
                cmake_content.append(f'\t\t{dependency}')
            cmake_content.append(')')
        if cpp.is_qt:
            cmake_content.extend(self._generate_cpp_qt_third_party_precompiled_archive(cpp))
        cmake_content.append('')
        return cmake_content

    def _generate_cpp_qt_third_party_precompiled_archive(self, cpp: CppTarget):
        cmake_content = []
        unpack_target_name = cpp.properties.get('unpack_target_name')
        exe_suffix = ".exe" if Env.platform.windows else ""
        # TODO: Merge the source_archive moc helper into the main automoc helper, but initially this was the only
        #  way I could get the source archive workflow working initially and didn't want to bother merging the two
        #  immediately. If ain't broke...
        if not self._cmake_qt_utils_module_file.parent.exists():
            self._cmake_qt_utils_module_file.parent.mkdir(parents=True)
        self._cmake_qt_utils_module_file.write_text(f"""{self._current_generated_file_header}
set(IPRM_QT_ROOT_DIR "${{CMAKE_BINARY_DIR}}/{cpp.root_relative_dir.path.as_posix()}" CACHE PATH "Root Qt Directory")
set(IPRM_QT_BIN_DIR "${{IPRM_QT_ROOT_DIR}}/{cpp.properties.get('bin_dir').path.as_posix()}" CACHE PATH "Root Qt Binary Directory")
set(IPRM_QT_MOC_EXECUTABLE "${{IPRM_QT_BIN_DIR}}/moc{exe_suffix}" CACHE PATH "Qt MOC Executable")
set(IPRM_QT_RCC_EXECUTABLE "${{IPRM_QT_BIN_DIR}}/rcc{exe_suffix}" CACHE PATH "Qt RCC Executable")
set(IPRM_QT_UIC_EXECUTABLE "${{IPRM_QT_BIN_DIR}}/uic{exe_suffix}" CACHE PATH "Qt UIC Executable")
set(IPRM_QT_UNPACK_TARGET_NAME {unpack_target_name} CACHE STRING "Qt Unpack Precompiled Archive Target Name")

{self._cpp_qt_automoc()}

# Source archive specific automoc helper fixing issue with CMake having to generate its target build system file(s) 
# twice, at least with Ninja, for the headers to actually get MOC'd
function(iprm_qt_automoc_source_archive target unpack_target)
	get_target_property(target_sources ${{target}} SOURCES)
	foreach(source ${{target_sources}})
		if(source MATCHES "\\.(h|hpp)$")
			get_filename_component(directory ${{source}} DIRECTORY)
			get_filename_component(filename ${{source}} NAME_WE)
			get_filename_component(ext ${{source}} EXT)
			set(moc_input "${{directory}}/${{filename}}${{ext}}")
			file(RELATIVE_PATH rel_directory ${{CMAKE_CURRENT_SOURCE_DIR}} ${{directory}})
			set(moc_output "${{CMAKE_CURRENT_BINARY_DIR}}/${{rel_directory}}/moc_${{filename}}.cpp")
			set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:third_k_editor_objects,INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")

            file(RELATIVE_PATH rel_moc_input "${{CMAKE_SOURCE_DIR}}" "${{moc_input}}")

			add_custom_command(
					OUTPUT ${{moc_output}}
					COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
					${{moc_includes}}
					${{moc_input}}
					-o ${{moc_output}}
					DEPENDS
					${{source}} ${{IPRM_QT_UNPACK_TARGET_NAME}} ${{unpack_target}}
					COMMENT "MOC ${{rel_moc_input}}"
					VERBATIM
					COMMAND_EXPAND_LISTS
			)
			target_sources(${{target}} PRIVATE ${{moc_output}})
		endif()
	endforeach()
endfunction()

{self._cpp_qt_autorcc()}

{self._cpp_qt_autouic()}
""")
        return cmake_content

    @classmethod
    def _add_archive_unpack_variables(cls, cpp: CppTarget):
        cmake_content = [
            f'set(extract_dir "{cls.current_bin_dir()}")'
        ]

        archive_dir = cpp.properties.get('archive_dir')
        archive_file = cpp.properties.get('archive_file')
        archive_file_path = cls.relative_src_path(archive_dir, archive_file)
        cmake_content.append(f'set(archive_file {archive_file_path})')

        unpack_target_name = cpp.properties.get('unpack_target_name')
        # TODO: Confirm if this is actually needed or does the output files being used as the custom target DEPENDS
        #  suffice, as we have to ensure the dependency graph is built up correctly. It may depend on the generator
        #  (e.g. Ninja needs it, Visual Studio doesn't), but leaving in for now as everything is working for all tested
        #  generators
        cmake_content.append(f'set(sentinel_file "${{extract_dir}}/{unpack_target_name}.sentinel")')
        cmake_content.append('set(archive_output_files ${sentinel_file})')
        return cmake_content

    @classmethod
    def _add_archive_unpack_command(cls, cpp: CppTarget):
        unpack_target_name = cpp.properties.get('unpack_target_name')
        cmake_content = [
            'add_custom_command(',
            '\tOUTPUT',
            '\t\t${archive_output_files}',
            '\tDEPENDS',
            '\t\t${archive_file}',
            '\tCOMMAND ${CMAKE_COMMAND} -E make_directory ${extract_dir}',
            '\tCOMMENT "Unpacking ${archive_file} to ${extract_dir}"',
            '\tCOMMAND ${CMAKE_COMMAND} -E tar xzf ${archive_file}',
            '\tCOMMAND ${CMAKE_COMMAND} -E touch ${sentinel_file}',
        ]
        patches_dict = cpp.properties.get('patches', {})
        if patches_dict:
            for patch_dir, patch_files in patches_dict.items():
                for patch_file in patch_files:
                    cmake_content.append(f'\tCOMMAND git apply {cls.relative_src_path(patch_dir, patch_file)}')
                    cmake_content.append(f'\tCOMMENT "Applying patch {patch_file}"')
        cmake_content.extend([
            '\tWORKING_DIRECTORY ${extract_dir}',
            '\tVERBATIM',
            '\tCOMMAND_EXPAND_LISTS',
            ')',
            f'add_custom_target({unpack_target_name} DEPENDS ${{sentinel_file}})',
            '',
        ])
        return cmake_content

    def _generate_cpp_third_party_imported(self, cpp: CppTarget):
        cmake_content = []
        target = cpp.name
        if cpp.is_precompiled_archive:
            if cpp.is_shared:
                cmake_content.append(f'add_library({target} SHARED IMPORTED GLOBAL)')
            elif cpp.is_static:
                cmake_content.append(f'add_library({target} STATIC IMPORTED GLOBAL)')
            elif cpp.is_app:
                cmake_content.append(f'add_executable({target} IMPORTED GLOBAL)')
            else:
                return cmake_content

            target_include_dirs = f'{target}_include_dirs'
            cmake_content.append(f'set({target_include_dirs}')
            include_paths = cpp.properties.get('include_paths')
            if include_paths:
                for include_path in include_paths:
                    cmake_content.append(f'\t\t{self.relative_bin_path(include_path)}')
                cmake_content.append(')')
            else:
                cmake_content[-1] += ')'
            # An unfortunate gimmick of CMake is the values set on the targets INTERFACE_INCLUDE_DIRECTORIES property
            # MUST exist on the filesystem at configure time, I tried using BUILD_INTERFACE generator expression to
            # hack around this, but no dice. Since this all happens in the current binary dir anyway there is no concern
            # about just creating the archive include directory up front, it's contents will eventually be populated after
            # extraction occurs (assuming we are imported from an archive source, which is the typical use case but not
            # the only scenario possible)
            cmake_content.append(f'foreach(include_dir IN LISTS {target_include_dirs})')
            cmake_content.append('\tfile(MAKE_DIRECTORY ${include_dir})')
            cmake_content.append('endforeach()')

            cmake_content.append(f'set_target_properties({target}')
            cmake_content.append('\tPROPERTIES')
            cmake_content.append(f'\t\tINTERFACE_INCLUDE_DIRECTORIES "${{{target_include_dirs}}}"')

            imported = cpp.properties.get('imported')
            lib_dir = imported.get('lib_dir', None)
            if lib_dir:
                lib_release, lib_debug = self._extract_precompiled_lib_artifact(imported)
                location_release = self.relative_bin_path(lib_dir, lib_release)
                cmake_content.append(f'\t\tIMPORTED_LOCATION_RELEASE {location_release}')
                cmake_content.append(f'\t\tIMPORTED_LOCATION_RELWITHDEBINFO {location_release}')
                cmake_content.append(f'\t\tIMPORTED_LOCATION_MINSIZEREL {location_release}')
                if lib_debug:
                    location_debug = self.relative_bin_path(lib_dir, lib_debug)
                    cmake_content.append(f'\t\tIMPORTED_LOCATION_DEBUG {location_debug}')
            implib_dir = imported.get('implib_dir', None)
            if implib_dir:
                implib_release, implib_debug = self._extract_precompiled_implib_artifact(imported)
                implib_release = self.relative_bin_path(implib_dir, implib_release)
                cmake_content.append(f'\t\tIMPORTED_IMPLIB_RELEASE {implib_release}')
                cmake_content.append(f'\t\tIMPORTED_IMPLIB_RELWITHDEBINFO {implib_release}')
                cmake_content.append(f'\t\tIMPORTED_IMPLIB_MINSIZEREL {implib_release}')
                if implib_debug:
                    implib_debug = self.relative_bin_path(implib_dir, implib_debug)
                    cmake_content.append(f'\t\tIMPORTED_IMPLIB_DEBUG {implib_debug}')
            cmake_content.append(')')

            unpack_target_name = cpp.properties.get('unpack_target_name', None)
            if unpack_target_name:
                cmake_content.append(f'add_dependencies({target} {unpack_target_name})')
        elif cpp.is_homebrew:
            lib = cpp.properties.get('homebrew_lib')
            brew_target = cpp.properties.get('homebrew_target')
            cmake_content.append(f'add_library({target} INTERFACE)')
            cmake_content.append(f'target_link_libraries({target}')
            cmake_content.append(f'\tINTERFACE')
            cmake_content.append(f'\t\t{brew_target}')
            cmake_content.append(f'\t\t{lib}')
            cmake_content.append(')')
            cmake_content.append('')
        elif cpp.is_pkgconfig:
            module = cpp.properties.get('pkconfig_module')
            lib = cpp.properties.get('pkconfig_lib')
            cmake_content.append(f'pkg_check_modules({module} REQUIRED {lib})')
            cmake_content.append(f'add_library({target} INTERFACE)')
            cmake_content.append(f'target_include_directories({target}')
            cmake_content.append(f'\tINTERFACE')
            cmake_content.append(f'\t\t${{{module}_INCLUDE_DIRS}}')
            cmake_content.append(')')
            cmake_content.append(f'target_link_directories({target}')
            cmake_content.append(f'\tINTERFACE')
            cmake_content.append(f'\t\t${{{module}_LIBRARY_DIRS}}')
            cmake_content.append(')')
            cmake_content.append(f'target_link_libraries({target}')
            cmake_content.append(f'\tINTERFACE')
            cmake_content.append(f'\t\t${{{module}_LIBRARIES}}')
            cmake_content.append(')')
            cmake_content.append('')
        return cmake_content

    def _generate_cpp_third_party_git(self, cpp: CppTarget):
        target = cpp.name
        repository = cpp.properties.get('git_repository')
        tag = cpp.properties.get('git_tag')
        target_git = f'{target}_git'

        # TODO: Make this happen at build time and use dependency clone marker for dependent libs
        # TODO: Just use the standard fetch content src dir variable and build the library up ourselves using the files
        #  and CppTarget type specified, just like we do with SCons/MSBuild for GTest AND PyBind, where the former is a
        #  static lib and the latter is just header only

        cmake_content = [
            'include(FetchContent)',
            'Set(FETCHCONTENT_QUIET FALSE)',
            'FetchContent_Declare(',
            f'\t{target_git}',
            f'\tGIT_REPOSITORY {repository}',
            f'\tGIT_TAG {tag}',
            ')',
            f'FetchContent_MakeAvailable({target_git})',
            f'add_library({target} INTERFACE)',
            f'target_link_libraries({target}',
            '\tINTERFACE',
        ]



        target_type = type(cpp).__name__
        if target_type == 'GTestThirdParty':
            cmake_content.append('\t\tgtest')
            cmake_content.append('\t\tgmock')
        elif target_type == 'PyBind11ThirdParty':
            cmake_content.append('\t\tpybind11::pybind11')
        else:
            pass
        cmake_content.append(')')
        cmake_content.append('')
        return cmake_content

    def _generate_cpp_third_party_homebrew(self, cpp: CppTarget):
        target = cpp.name
        target_brew = f'{target}_brew'
        cmake_content = [
            'execute_process(',
            '\tCOMMAND brew --prefix',
            '\tOUTPUT_VARIABLE BREW_PREFIX',
            '\tOUTPUT_STRIP_TRAILING_WHITESPACE',
            ')',
            'set(BREW_INCLUDE_DIR "${BREW_PREFIX}/include")',
            'set(BREW_LIB_DIR "${BREW_PREFIX}/lib")',
            f'add_library({target_brew} INTERFACE)',
            f'target_include_directories({target_brew}',
            '\tINTERFACE',
            '\t\t${BREW_INCLUDE_DIR}',
            ')',
            f'target_link_directories({target_brew}',
            '\tINTERFACE',
            '\t\t${BREW_LIB_DIR}',
            ')',
        ]
        package = cpp.properties.get('homebrew_package')
        cmake_content.extend([
            f'target_link_directories({target_brew}',
            '\tINTERFACE',
            f'\t\t${{BREW_LIB_DIR}}/{package}',
            f')',
        ])
        cmake_content.append(f'add_library({target} INTERFACE)')
        cmake_content.append(f'target_link_libraries({target}')
        cmake_content.append(f'\tINTERFACE')
        cmake_content.append(f'\t\t{target_brew}')
        # TODO: Can we simplify and remove this property by just using dependencies instead?
        #  dependencies = cpp.dependencies
        libs = cpp.properties.get('homebrew_libs')
        if not cpp.is_qt:
            for lib in libs:
                cmake_content.append(f'\t\t{target}_{lib}')
            cmake_content.append(')')
        if cpp.is_qt:
            cmake_content.append(f'\t\t"-F${{BREW_LIB_DIR}}"')
            strip_prefix = lambda text, prefix: text[len(prefix):] if text.lower().startswith(prefix.lower()) else text
            qt_modules = [f'Qt{strip_prefix(lib, package)}' for lib in libs]
            for qt_module in qt_modules:
                cmake_content.append(f'\t\t"-framework {qt_module}"')
            cmake_content.append(')')
            cmake_content.extend([
                f'target_include_directories({target}',
                '\tINTERFACE',
            ])
            for qt_module in qt_modules:
                cmake_content.append(f'\t\t${{BREW_INCLUDE_DIR}}/{qt_module}')
            cmake_content.append(')')

            if not self._cmake_qt_utils_module_file.parent.exists():
                self._cmake_qt_utils_module_file.parent.mkdir(parents=True)
            # TODO: Maybe use python pkg-config library instead so each target that includes the
            #   qt utils doesn't need to invoke the process, that way we can just hardcode the
            #   module file. That being said, it is cheap/quick, so this is fine for now
            self._cmake_qt_utils_module_file.write_text(f"""{self._current_generated_file_header}
execute_process(
	COMMAND brew --prefix
	OUTPUT_VARIABLE BREW_PREFIX
	OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(QT6_QMAKE_BIN "${{BREW_PREFIX}}/bin/qmake")                  
execute_process(
    COMMAND ${{QT6_QMAKE_BIN}} -query QT_INSTALL_DATA
    OUTPUT_VARIABLE HOMEBREW_QT_ROOT_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
execute_process(
  COMMAND ${{QT6_QMAKE_BIN}} -query QT_INSTALL_LIBEXECS
  OUTPUT_VARIABLE QT6_LIBEXECDIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(IPRM_QT_ROOT_DIR "${{HOMEBREW_QT_ROOT_DIR}}" CACHE PATH "Root Qt Directory")
set(IPRM_QT_MOC_EXECUTABLE "${{QT6_LIBEXECDIR}}/moc" CACHE PATH "Qt MOC Executable")
set(IPRM_QT_RCC_EXECUTABLE "${{QT6_LIBEXECDIR}}/rcc" CACHE PATH "Qt RCC Executable")
set(IPRM_QT_UIC_EXECUTABLE "${{QT6_LIBEXECDIR}}/uic" CACHE PATH "Qt UIC Executable")

{self._cpp_qt_automoc()}

# Source archive specific automoc helper fixing issue with CMake having to generate its target build system file(s) 
# twice, at least with Ninja, for the headers to actually get MOC'd
function(iprm_qt_automoc_source_archive target unpack_target)
	get_target_property(target_sources ${{target}} SOURCES)
	foreach(source ${{target_sources}})
		if(source MATCHES "\\.(h|hpp)$")
			get_filename_component(directory ${{source}} DIRECTORY)
			get_filename_component(filename ${{source}} NAME_WE)
			get_filename_component(ext ${{source}} EXT)
			set(moc_input "${{directory}}/${{filename}}${{ext}}")
			file(RELATIVE_PATH rel_directory ${{CMAKE_CURRENT_SOURCE_DIR}} ${{directory}})
			set(moc_output "${{CMAKE_CURRENT_BINARY_DIR}}/${{rel_directory}}/moc_${{filename}}.cpp")
			set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:third_k_editor_objects,INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")

            file(RELATIVE_PATH rel_moc_input "${{CMAKE_SOURCE_DIR}}" "${{moc_input}}")

			add_custom_command(
					OUTPUT ${{moc_output}}
					COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
					${{moc_includes}}
					${{moc_input}}
					-o ${{moc_output}}
					DEPENDS
					${{source}} ${{unpack_target}}
					COMMENT "MOC ${{rel_moc_input}}"
					VERBATIM
					COMMAND_EXPAND_LISTS
			)
			target_sources(${{target}} PRIVATE ${{moc_output}})
		endif()
	endforeach()
endfunction()

{self._cpp_qt_autorcc()}

{self._cpp_qt_autouic()}
""")
        cmake_content.append('')
        return cmake_content

    def _generate_cpp_third_party_pkgconfig(self, cpp: CppTarget):
        target = cpp.name
        cmake_content = []
        cmake_content.append(f'add_library({target} INTERFACE)')
        cmake_content.append(f'target_link_libraries({target}')
        cmake_content.append(f'\tINTERFACE')
        modules = cpp.properties.get('pkconfig_modules')
        for module in modules:
            cmake_content.append(f'\t\t{target}_{module}')
        cmake_content.append(')')
        cmake_content.append('')
        cmake_content.append('find_package(PkgConfig REQUIRED)')

        # TODO: Create a more general way for third party targets to include extra dependencies
        dependencies = cpp.dependencies
        other_dependencies = []
        with platform_context(Env.platform):
            for dependency in dependencies:
                dependency_obj = Session.get_object(dependency)
                if not dependency_obj or dependency_obj.is_pkgconfig:
                    continue
                other_dependencies.append(dependency_obj.name)
        if other_dependencies:
            cmake_content.append(f'target_link_libraries({target}')
            cmake_content.append(f'\tINTERFACE')
            for dependency in other_dependencies:
                cmake_content.append(f'\t\t{dependency}')
            cmake_content.append(')')
        # NOTE: Windows does not have pkg-config support currently
        if not Env.platform.windows and cpp.is_qt:
            if not self._cmake_qt_utils_module_file.parent.exists():
                self._cmake_qt_utils_module_file.parent.mkdir(parents=True)
            # TODO: Maybe use python pkg-config library instead so each target that includes the 
            #   qt utils doesn't need to invoke the process, that way we can just hardcode the 
            #   module file. That being said, it is cheap/quick, so this is fine for now
            self._cmake_qt_utils_module_file.write_text(f"""{self._current_generated_file_header}                          
execute_process(
    COMMAND bash -c "dirname $($(pkg-config --variable=bindir Qt6Core)/qmake -query QT_INSTALL_PLUGINS)"
    OUTPUT_VARIABLE PKCONFIG_QT_ROOT_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
execute_process(
  COMMAND pkg-config --variable=libexecdir Qt6Core
  OUTPUT_VARIABLE QT6_LIBEXECDIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(IPRM_QT_ROOT_DIR "${{PKCONFIG_QT_ROOT_DIR}}" CACHE PATH "Root Qt Directory")
set(IPRM_QT_MOC_EXECUTABLE "${{QT6_LIBEXECDIR}}/moc" CACHE PATH "Qt MOC Executable")
set(IPRM_QT_RCC_EXECUTABLE "${{QT6_LIBEXECDIR}}/rcc" CACHE PATH "Qt RCC Executable")
set(IPRM_QT_UIC_EXECUTABLE "${{QT6_LIBEXECDIR}}/uic" CACHE PATH "Qt UIC Executable")

{self._cpp_qt_automoc()}

# Source archive specific automoc helper fixing issue with CMake having to generate its target build system file(s) 
# twice, at least with Ninja, for the headers to actually get MOC'd
function(iprm_qt_automoc_source_archive target unpack_target)
	get_target_property(target_sources ${{target}} SOURCES)
	foreach(source ${{target_sources}})
		if(source MATCHES "\\.(h|hpp)$")
			get_filename_component(directory ${{source}} DIRECTORY)
			get_filename_component(filename ${{source}} NAME_WE)
			get_filename_component(ext ${{source}} EXT)
			set(moc_input "${{directory}}/${{filename}}${{ext}}")
			file(RELATIVE_PATH rel_directory ${{CMAKE_CURRENT_SOURCE_DIR}} ${{directory}})
			set(moc_output "${{CMAKE_CURRENT_BINARY_DIR}}/${{rel_directory}}/moc_${{filename}}.cpp")
			set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:third_k_editor_objects,INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")

            file(RELATIVE_PATH rel_moc_input "${{CMAKE_SOURCE_DIR}}" "${{moc_input}}")

			add_custom_command(
					OUTPUT ${{moc_output}}
					COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
					${{moc_includes}}
					${{moc_input}}
					-o ${{moc_output}}
					DEPENDS
					${{source}} ${{unpack_target}}
					COMMENT "MOC ${{rel_moc_input}}"
					VERBATIM
					COMMAND_EXPAND_LISTS
			)
			target_sources(${{target}} PRIVATE ${{moc_output}})
		endif()
	endforeach()
endfunction()

{self._cpp_qt_autorcc()}

{self._cpp_qt_autouic()}
""")
        cmake_content.append('')
        return cmake_content

    def _generate_cpp_third_party_system(self, cpp: CppTarget):

        cmake_content = []
        if Env.platform.linux:
            if cpp.is_dpkg:
                cmake_content.extend(self._generate_cpp_third_party_linux_system(cpp, 'dpkg', '-L'))
            elif cpp.is_rpm:
                cmake_content.extend(self._generate_cpp_third_party_linux_system(cpp, 'rpm', '-ql'))
        return cmake_content

    def _generate_cpp_third_party_linux_system(self, cpp: CppTarget, package_manager, package_query_args):
        target = cpp.name
        package = cpp.properties.get(f'{package_manager}_package')
        package_upper = package.upper()
        package_manager_upper = package_manager.upper()
        package_library_dirs = f'{package_manager_upper}_{package_upper}_LIBRARY_DIRS'
        package_libraries = f'{package_manager_upper}_{package_upper}_LIBRARIES'
        # TODO: Support finding static libs, executables, include dirs, and multiple lib dirs (if any packages have that)
        cmake_content = [
            'execute_process(',
            f"\tCOMMAND \"{package_manager} {package_query_args} {package} | grep '\\.so' | head -1 | xargs dirname | sort -u\"",
            f'\tOUTPUT_VARIABLE {package_library_dirs}',
            '\tOUTPUT_STRIP_TRAILING_WHITESPACE',
            ')',
            'execute_process(',
            f"\tCOMMAND \"{package_manager} {package_query_args}  {package} | grep '\\.so' | xargs -n1 basename | sed -E 's/(.+)\\.so.*/\\\\1/g' | sort -u\"",
            f'\tOUTPUT_VARIABLE {package_libraries}',
            '\tOUTPUT_STRIP_TRAILING_WHITESPACE',
            ')',
            f'string(REPLACE "\\n" ";" {package_libraries} "${{{package_libraries}}}")',
            f'add_library({target} INTERFACE)',
            f'target_link_directories({target}',
            '\tINTERFACE',
            f'\t\t${{{package_library_dirs}}}',
            ')',
            f'target_link_libraries({target}',
            '\tINTERFACE',
            f'\t\t${{{package_libraries}}}',
            ')',
            '',
        ]
        return cmake_content

    @classmethod
    def _cpp_add_sources(cls, cpp: CppTarget, key: str):
        cmake_content_sources = []
        sources_dict = cpp.properties.get(key, {})
        if sources_dict:
            cmake_content_sources.append(f'target_sources({cpp.name}')
            cmake_content_sources.append(f'\tPRIVATE')
            for src_dir, src_files in sources_dict.items():
                for src_file in src_files:
                    cmake_content_sources.append(f'\t\t{cls.relative_src_path(src_dir, src_file)}')
            cmake_content_sources.append(')')
        return cmake_content_sources

    @classmethod
    def _cpp_source_file_exts(cls):
        source_file_exts = ProjectModel._cpp_source_file_exts()
        source_file_exts.extend(['qrc', 'ui', 'rc'])
        return source_file_exts

    @classmethod
    def _cpp_runtime_files(cls, cpp: CppTarget):
        runtime_files = set()
        for target in cls._cpp_get_dependency_objects(cpp):
            runtime_files_dict = target.properties.get('runtime_files', {})
            if runtime_files_dict:
                for files_dir, files in runtime_files_dict.items():
                    for runtime_file in files:
                        runtime_files.add(cls.relative_bin_path(files_dir, runtime_file))
            runtime_files.update(cls._cpp_runtime_files(target))
        return runtime_files

    @classmethod
    def _cpp_runtime_paths(cls, cpp: CppTarget):
        runtime_paths = set()
        for target in cls._cpp_get_dependency_objects(cpp):
            runtime_paths_list = target.properties.get('runtime_paths', [])
            if runtime_paths_list:
                for runtime_path_dir in runtime_paths_list:
                    runtime_paths.add(cls.relative_bin_path(runtime_path_dir))
            runtime_paths.update(cls._cpp_runtime_paths(target))
        return runtime_paths

    @classmethod
    def _cpp_get_dependency_objects(cls, cpp: CppTarget):
        targets: list[CppTarget] = []
        dependencies = cpp.dependencies
        with platform_context(Env.platform):
            for dependency in dependencies:
                dependency_obj = Session.get_object(dependency)
                if not dependency_obj:
                    continue
                if dependency_obj.is_cpp:
                    targets.append(dependency_obj)
        return targets

    @classmethod
    def _cpp_qt_automoc(cls):
        return f"""function(iprm_qt_automoc target)
    get_target_property(target_sources ${{target}} SOURCES)
    set(headers_to_moc "")

    set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:${{target}},INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")

    foreach(source_file ${{target_sources}})
        if(source_file MATCHES "\\\\.(h|hpp|hxx)$")
            if(IS_ABSOLUTE ${{source_file}})
                set(header_path "${{source_file}}")
            else()
                set(header_path "${{CMAKE_CURRENT_SOURCE_DIR}}/${{source_file}}")
            endif()

            if(EXISTS "${{header_path}}")
                file(READ "${{header_path}}" header_contents)
                if(header_contents MATCHES "Q_OBJECT")
                    list(APPEND headers_to_moc "${{header_path}}")
                endif()
            endif()
        endif()
    endforeach()

    foreach(header_path ${{headers_to_moc}})
        get_filename_component(header_name_we ${{header_path}} NAME_WE)
        set(moc_file "${{CMAKE_CURRENT_BINARY_DIR}}/moc_${{header_name_we}}.cpp")

        file(RELATIVE_PATH rel_header_path "${{CMAKE_SOURCE_DIR}}" "${{header_path}}")

        add_custom_command(
                OUTPUT ${{moc_file}}
                COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
                ARGS ${{moc_includes}} -o ${{moc_file}} ${{header_path}}
                DEPENDS ${{header_path}} ${{IPRM_QT_UNPACK_TARGET_NAME}}
                COMMENT "MOC ${{rel_header_path}}"
                VERBATIM
                COMMAND_EXPAND_LISTS
        )
        target_sources(${{target}} PRIVATE ${{moc_file}})
    endforeach()
endfunction()
"""

    @classmethod
    def _cpp_qt_autorcc(cls):
        return f"""function(iprm_qt_autorcc target)
    get_target_property(target_sources ${{target}} SOURCES)
    foreach(source_file ${{target_sources}})
        if(source_file MATCHES "\\\\.qrc$")
            if(IS_ABSOLUTE ${{source_file}})
                set(qrc_file "${{source_file}}")
            else()
                set(qrc_file "${{CMAKE_CURRENT_SOURCE_DIR}}/${{source_file}}")
            endif()

            get_filename_component(qrc_name_we ${{qrc_file}} NAME_WE)
            set(rcc_cpp_file "${{CMAKE_CURRENT_BINARY_DIR}}/qrc_${{qrc_name_we}}.cpp")
            
            file(RELATIVE_PATH rel_qrc_file "${{CMAKE_SOURCE_DIR}}" "${{qrc_file}}")

            add_custom_command(
                    OUTPUT ${{rcc_cpp_file}}
                    COMMAND ${{IPRM_QT_RCC_EXECUTABLE}}
                    ARGS -name ${{qrc_name_we}} -o ${{rcc_cpp_file}} ${{qrc_file}}
                    DEPENDS ${{qrc_file}} ${{IPRM_QT_UNPACK_TARGET_NAME}}
                    COMMENT "RCC ${{rel_qrc_file}}"
                    VERBATIM
            )
            target_sources(${{target}} PRIVATE ${{rcc_cpp_file}})
        endif()
    endforeach()
endfunction()
"""

    @classmethod
    def _cpp_qt_autouic(cls):
        return f"""function(iprm_qt_autouic target)
    get_target_property(target_sources ${{target}} SOURCES)
    foreach(source_file ${{target_sources}})
        if(source_file MATCHES "\\\\.ui$")
            if(IS_ABSOLUTE ${{source_file}})
                set(ui_file "${{source_file}}")
            else()
                set(ui_file "${{CMAKE_CURRENT_SOURCE_DIR}}/${{source_file}}")
            endif()

            get_filename_component(ui_name_we ${{ui_file}} NAME_WE)
            set(ui_h_file "${{CMAKE_CURRENT_BINARY_DIR}}/ui_${{ui_name_we}}.h")

            file(RELATIVE_PATH rel_ui_file "${{CMAKE_SOURCE_DIR}}" "${{ui_file}}")

            add_custom_command(
                    OUTPUT ${{ui_h_file}}
                    COMMAND ${{IPRM_QT_UIC_EXECUTABLE}}
                    ARGS -o ${{ui_h_file}} ${{ui_file}}
                    DEPENDS ${{ui_file}} ${{IPRM_QT_UNPACK_TARGET_NAME}}
                    COMMENT "UIC ${{rel_ui_file}}"
                    VERBATIM
            )
            target_include_directories(${{target}} PRIVATE ${{CMAKE_CURRENT_BINARY_DIR}})

            set_property(TARGET ${{target}} APPEND PROPERTY ADDITIONAL_CLEAN_FILES ${{ui_h_file}})
            add_custom_target(
                    ${{target}}_ui_${{ui_name_we}} ALL DEPENDS ${{ui_h_file}}
            )
            add_dependencies(${{target}} ${{target}}_ui_${{ui_name_we}})
        endif()
    endforeach()
endfunction()
"""

    def _cpp_qt_generate_sources(self, cpp: CppTarget, target=None):
        cmake_content = []
        qt_library = cpp.properties.get('qt_library')
        target = target if target else cpp.name
        with platform_context(Env.platform):
            qt_library_target = Session.get_object(qt_library)
            if qt_library_target is None:
                return cmake_content

            from iprm.api.cpp import QtThirdParty
            cmake_content.append('include(qt_utils)')
            if qt_library_target.properties.get(QtThirdParty.MOC, False):
                if cpp.is_source_archive:
                    unpack_target_name = cpp.properties.get('unpack_target_name')
                    cmake_content.append(f'iprm_qt_automoc_source_archive({target} {unpack_target_name})')
                else:
                    cmake_content.append(f'iprm_qt_automoc({target})')
            if qt_library_target.properties.get(QtThirdParty.RCC, False):
                cmake_content.append(f'iprm_qt_autorcc({target})')
            if qt_library_target.properties.get(QtThirdParty.UIC, False):
                cmake_content.append(f'iprm_qt_autouic({target})')
            if (cpp.is_app or cpp.is_test) and qt_library_target.properties.get(QtThirdParty.CONF, False):
                qt_conf_content = """[Paths]
Prefix=@IPRM_QT_ROOT_DIR@
Plugins=@IPRM_QT_ROOT_DIR@/plugins
"""
                qt_conf_template_file = self._current_generate_dir / 'qt.conf.in'
                qt_conf_template_file.write_text(qt_conf_content)
                output_dir = cpp.properties.get('output_dir', None)
                if output_dir:
                    cmake_content.append(
                        f'configure_file("${{CMAKE_CURRENT_SOURCE_DIR}}/qt.conf.in" {self.relative_src_path(output_dir, "qt.conf")} @ONLY)')
                else:
                    cmake_content.append(
                        'configure_file("${CMAKE_CURRENT_SOURCE_DIR}/qt.conf.in" "${CMAKE_CURRENT_BINARY_DIR}/qt.conf" @ONLY)')
            if not Env.platform.windows:
                # TODO: Generalize this RPATH infrastructure in the first_party section
                cmake_content.extend([
                    f'set_target_properties({target}',
                    '\tPROPERTIES',
                ])
                cmake_content.append(f'\t\tBUILD_RPATH "${{IPRM_QT_ROOT_DIR}}/lib"')
                if Env.platform.macos:
                    cmake_content.append(f'\t\tMACOSX_RPATH ON')
                cmake_content.append(')')
        return cmake_content

    @classmethod
    def _cpp_add_ms_crt(cls, cpp: CppTarget):
        cmake_content = []
        target = cpp.name
        # TODO: Don't set compile-time properties for targets that don't get built by us (e.g.third party pre-compiled
        #  content or header-only libraries)
        if cpp.compiler_supports_property(cpp.compiler_flag, 'microsoft_crt'):
            from iprm.api.cpp import MicrosoftCRuntime
            crt = cpp.properties.get('microsoft_crt', MicrosoftCRuntime.DYNAMIC)
            if crt == MicrosoftCRuntime.DYNAMIC:
                cmake_content.append(f'set_target_properties({target} PROPERTIES')
                cmake_content.append('\tMSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL"')
                cmake_content.append(')')
            elif crt == MicrosoftCRuntime.STATIC:
                cmake_content.append(f'set_target_properties({target} PROPERTIES')
                cmake_content.append('\tMSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"')
                cmake_content.append(')')
        return cmake_content

    def _generate_rust(self, rust: RustTarget):
        if not rust.compiler_supports_property(rust.compiler_flag, 'crate'):
            return []

        target = rust.name
        manifest_dir, cargo_file = rust.properties.get('manifest')
        manifest_file = f'"{self.current_src_dir()}/{cargo_file}"' \
            if manifest_dir == CurrentSourceDir() else \
            f'"{self.current_src_dir()}/{manifest_dir.path.as_posix()}/{cargo_file}"'

        # TODO: For now assumes the output is an executable and main.rs is in it's standard place, allow for
        #  static/shared libs too
        exe_suffix = '.exe' if Env.platform.windows else ''
        cargo_locked = rust.properties.get('cargo_locked', False)
        cmake_content = [
            'find_program(CARGO_EXECUTABLE cargo REQUIRED)',
            f'set(CARGO_TARGET_DIR {self.current_bin_dir()})',
            f'set(CARGO_TOML_PATH {manifest_file})',
            f'if(CMAKE_BUILD_TYPE MATCHES "Release|MinSizeRel|RelWithDebInfo")',
            '\tset(CARGO_PROFILE "release")',
            f'\tset(RUST_EXE_PATH ${{CARGO_TARGET_DIR}}/release/{target}{exe_suffix})',
            f'else()',
            '\tset(CARGO_PROFILE "dev")',
            f'\tset(RUST_EXE_PATH ${{CARGO_TARGET_DIR}}/debug/{target}{exe_suffix})',
            f'endif()',
            'add_custom_command(',
            '\tOUTPUT ${RUST_EXE_PATH}',
            '\tCOMMAND ${CARGO_EXECUTABLE} build',
            '\t\t--manifest-path ${CARGO_TOML_PATH}',
            '\t\t--target-dir ${CARGO_TARGET_DIR}',
            f'\t\t--profile ${{CARGO_PROFILE}}{'\n--locked' if cargo_locked else ''}',
            # TODO: Allow for linking with libraries this depends on
            f'\tWORKING_DIRECTORY {self.current_src_dir()}',
            '\tDEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/main.rs ${CARGO_TOML_PATH}',
            '\tVERBATIM',
            ')',
            f'add_custom_target({target} ALL DEPENDS ${{RUST_EXE_PATH}})',
            f'target_sources({target}',
            '\tPRIVATE',
            f'\t\t{manifest_file}',
        ]
        sources_dict = rust.properties.get('sources', {})
        if sources_dict:
            for src_dir, src_files in sources_dict.items():
                for src_file in src_files:
                    cmake_content.append(f'\t\t{self.relative_src_path(src_dir, src_file)}')
        cmake_content.append(')')

        # NOTE: CMake does not natively support Rust, and there is only a single production ready compiler at the
        #  moment, so don't bother trying to explicitly set the target-specific compiler
        cmake_content.extend(self._generate_target(rust))
        cmake_content.append('')
        return cmake_content
