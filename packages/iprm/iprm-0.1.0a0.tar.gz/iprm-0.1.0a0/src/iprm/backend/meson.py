"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from itertools import zip_longest
from pathlib import Path
from typing import cast, Optional
from iprm.core.session import Session
from iprm.util.env import Env
from iprm.util.platform import platform_context
from iprm.util.dir import Dir, CurrentSourceDir, CurrentBinaryDir
from iprm.util.compiler import EMSCRIPTEN
from iprm.util.wasm import run_html_wasm_script
from iprm.backend.backend import ProjectModel
from iprm.util.loader import Loader
from iprm.api.project import Project, SubDir
from iprm.api.target import Target
from iprm.api.cpp import CppTarget, QtThirdParty
from iprm.api.rust import RustTarget


class Meson(ProjectModel):
    NATIVE_FILE_NAME = 'meson-native.ini'
    WASM_CROSS_FILE_NAME = 'meson-cross-wasm.ini'
    OPTIONS_FILE_NAME = 'meson.options'

    MESON_RUN_ENV = 'meson_run_env'

    _meson_file = 'meson.build'

    _meson_subprojects_dir: Optional[Path] = None

    def __init__(self, native_loader: Loader, **kwargs):
        kwargs['build_dir'] = 'builddir'
        super().__init__(native_loader, **kwargs)
        Meson._meson_subprojects_dir = Path(self.project_dir_str) / 'subprojects'

    @classmethod
    def generator_ninja(cls):
        return 'ninja'

    @classmethod
    def generator_xcode(cls):
        return 'xcode'

    @classmethod
    def generator_visual_studio(cls):
        return 'vs2022'

    @classmethod
    def generator_unix_makefile(cls):
        raise NotImplementedError('Meson does not natively support using Make as a backend')

    def _generate_file_name(self):
        return self._meson_file

    @classmethod
    def generate_file_exts(cls) -> list[str]:
        return [cls._meson_file]

    @property
    def release_build_type(self):
        return 'release'

    @classmethod
    def supports_posix_paths(cls):
        return True

    @classmethod
    def src_dir(cls):
        # TODO: Implement this when first scenario comes up where it is needed
        return NotImplementedError('Meson has not implemented src_dir()')

    @classmethod
    def current_src_dir(cls):
        return 'meson.current_source_dir()'

    # TODO: Consolidate the relative_*_path methods to share most of their code

    @classmethod
    def relative_src_path(cls, dir_path: Dir, leaf_path: str = None):
        if dir_path == CurrentSourceDir():
            leaf = '' if leaf_path is None else f" / '{leaf_path}'"
            return f"{cls.current_src_dir()}{leaf}"
        path = dir_path.path if leaf_path is None else dir_path.path.joinpath(leaf_path)
        return cls.current_src_dir() \
            if dir_path == CurrentSourceDir() \
            else f"{cls.current_src_dir()} / '{path.as_posix()}'"

    @classmethod
    def bin_dir(cls):
        # TODO: Implement this when first scenario comes up where it is needed
        return NotImplementedError('Meson has not implemented bin_dir()')

    @classmethod
    def current_bin_dir(cls):
        return 'meson.current_build_dir()'

    @classmethod
    def relative_bin_path(cls, dir_path: Dir, leaf_path: str = None):
        if dir_path == CurrentBinaryDir():
            leaf = '' if leaf_path is None else f" / '{leaf_path}'"
            return f"{cls.current_bin_dir()}{leaf}"
        path = dir_path.path if leaf_path is None else dir_path.path.joinpath(leaf_path)
        return cls.current_bin_dir() \
            if dir_path == CurrentBinaryDir() \
            else f"{cls.current_bin_dir()} / '{path.as_posix()}'"

    @classmethod
    def configure(cls, **kwargs):
        generator = kwargs.get('generator')
        srcdir = kwargs.get('srcdir')
        bindir = kwargs.get('bindir')
        cmd = [
            'meson',
            'setup',
            '--reconfigure',
            srcdir,
            bindir,
            f'--backend={generator}',
            f'--buildtype={cls.build_type(**kwargs)}',
        ]

        platform_ctx = kwargs.get('platform_ctx')
        if platform_ctx.wasm:
            cross_file_path = str(Path(srcdir) / cls.WASM_CROSS_FILE_NAME)
            cmd.append(f'--cross-file')
            cmd.append(f'"{cross_file_path}"')
        else:
            native_file_path = str(Path(srcdir) / cls.NATIVE_FILE_NAME)
            cmd.append(f'--native-file')
            cmd.append(f'"{native_file_path}"')
        return cls._run_command(cmd, platform_ctx)

    @classmethod
    def build(cls, **kwargs):
        bindir = kwargs.get('bindir')
        target = kwargs.get('target', None)
        cmd = [
            'meson',
            'compile',
            '-C',
            bindir,
            f'-j{cls.num_procs(**kwargs)}'
        ]
        if target:
            cmd.append(target)
        platform_ctx = kwargs.get('platform_ctx')
        return cls._run_command(cmd, platform_ctx)

    @classmethod
    def _default_build_type(cls):
        cls._release_build_type()

    @classmethod
    def _release_build_type(cls):
        return 'release'

    @classmethod
    def _debug_build_type(cls):
        return 'debug'

    @classmethod
    def test(cls, **kwargs):
        bindir = kwargs.get('bindir')
        cmd = [
            'meson',
            'test',
            '-C',
            bindir,
        ]
        return cls._run_command(cmd)

    @classmethod
    def install(cls, **kwargs):
        # TODO: impl install
        pass

    def _generate_project(self, project: Project):
        # https://github.com/mesonbuild/meson/issues/1752#issuecomment-1216718818
        # Unfortunately, Meson has quite a cumbersome way to specify the compiler,
        # it essentially forces you to use CMakes toolchain file concept, as it has no
        # inline build script method to set your compiler. It would be really nice if
        # it was done in the default_options section of the project() function.
        # Maybe one day!
        native_file_path = project.root_dir / self.NATIVE_FILE_NAME
        native_file_content = [
            '[binaries]',
        ]
        if project.cpp_enabled:
            native_file_content.append(f"cpp = '{project.cpp_compiler_binary()}'")
        if project.rust_enabled:
            native_file_content.append(f"rust = '{project.rust_compiler_binary()}'")
        native_file_content.append('')
        native_file_path.write_text(f'{self._current_generated_file_header}\n')
        native_file_path.write_text('\n'.join(native_file_content))

        # https://github.com/mesonbuild/meson/blob/master/cross/wasm.txt
        if project.cpp_compiler_flag() == EMSCRIPTEN:
            cross_file_path = project.root_dir / self.WASM_CROSS_FILE_NAME
            import platform

            suffix = '.bat' if platform.system() == "Windows" else ''
            cross_file_content = [
                '[binaries]',
                f"c = 'emcc{suffix}'",
                f"cpp = 'em++{suffix}'",
                f"ar = 'emar{suffix}'",
                '',
                '[build-in options]',
                'c_args = []',
                "c_link_args = ['-sEXPORT_ALL=1']",
                'cpp_args = []',
                "cpp_link_args = ['-sEXPORT_ALL=1']",
                '',
                '[host_machine]',
                "system = 'emscripten'",
                "cpu_family = 'wasm32'",
                "cpu = 'wasm32'",
                "endian = 'little'",
                '',
            ]
            cross_file_path.write_text(f'{self._current_generated_file_header}\n')
            cross_file_path.write_text('\n'.join(cross_file_content))

        meson_content = [
            f"project('{project.name}', ",
        ]
        langs_dict = project.properties.get('languages', {})
        meson_content_def_options = ["\tdefault_options : [\n"]
        cpp_std_conformance = False
        wasm_emscripten = project.cpp_compiler_flag() == EMSCRIPTEN
        if langs_dict:
            meson_content[-1] += '['
            langs_list = list(langs_dict.items())
            for (lang_type, lang_props), next_lang in zip_longest(langs_list, langs_list[1:], fillvalue=None):
                if lang_type == CppTarget.__name__:
                    standard = lang_props.get(CppTarget.STANDARD, None)
                    if standard:
                        meson_content_def_options[-1] += f"\t\t'cpp_std=c++{standard}',\n"
                    cpp_std_conformance = lang_props.get('conformance')
                    meson_content[-1] += "'cpp', "
                elif not wasm_emscripten and lang_type == RustTarget.__name__:
                    meson_content[-1] += "'rust', "
            meson_content[-1] += '],'

        meson_content_def_options[-1] += '\t]'

        meson_content.append(f"\tversion : '{project.properties.get('version', '0.1.0')}',")
        meson_content.extend(meson_content_def_options)
        meson_content.append(f')')
        meson_content.append('')

        # TODO: is this the best equivalent to what CMake can have? Or is there something better
        description = project.properties.get('description', None)
        if description:
            meson_content.append(f"summary('description', '{description}')")

        url = project.properties.get('url', None)
        if url:
            meson_content.append(f"summary('homepage_url', '{url}')")

        if Env.platform.windows and cpp_std_conformance:
            meson_content.append("if meson.get_compiler('cpp').get_id() == 'msvc'")
            meson_content.append("\tadd_project_arguments('/Zc:__cplusplus', '/permissive-', language : 'cpp')")
            meson_content.append('endif')

        meson_content.append(f'{self.MESON_RUN_ENV} = environment()')

        # NOTE: From initial testing with Visual Studio, it looks like Meson automatically creates the projects
        #   relative to their folder hierarchy, where-as we have to explicitly do that in CMake, otherwise
        #   everything gets inline

        self._meson_subprojects_dir.mkdir(exist_ok=True)
        options = project.properties.get('options', {})
        if options:
            options_file = project.root_dir / self.OPTIONS_FILE_NAME
            for opt_name, opt_config in options.items():
                options_file.write_text(f"option('{opt_name}', ")
                opt_default = opt_config.get('default')
                opt_type = opt_config.get('type')
                if opt_type == bool:
                    options_file.write_text("type: 'boolean', ")
                    options_file.write_text(f'value: {"true" if opt_default else "false"}, ')
                elif opt_type == int:
                    options_file.write_text("type: 'integer', ")
                    options_file.write_text(f'value: {str(opt_default)}, ')
                elif opt_type == str:
                    options_file.write_text("type: 'string', ")
                    options_file.write_text(f"value: '{opt_default}', ")
                opt_description = opt_config.get('description')
                options_file.write_text(f"description: '{opt_description}')")
                options_file.write_text('\n')
        meson_content.append('')
        return meson_content

    def _generate_subdir(self, subdir: SubDir):
        meson_content = []
        dir_name = subdir.properties.get('dir_name', [])
        if dir_name:
            meson_content.append(f"subdir('{dir_name}')")
        return meson_content

    def _generate_target(self, target: Target):
        return []

    def _generate_cpp(self, cpp: CppTarget):
        first_party = not cpp.is_third_party
        if first_party:
            return self._generate_cpp_first_party(cpp)
        else:
            return self._generate_cpp_third_party(cpp)

    def _generate_cpp_first_party(self, cpp: CppTarget):
        target = cpp.name
        target_cpp_flags = f'{target}_cpp_flags'
        target_link_flags = f'{target}_link_flags'
        meson_content = [
            f'{target_cpp_flags} = []',
            f'{target_link_flags} = []'
        ]

        # TODO: each set for these properties (defines, include_paths, dependencies) will either be transitive or not,
        #  but for now just hardcode to always transitive for include_paths and dependencies and non-transitive for
        #  defines
        defines = cpp.properties.get('defines')
        if defines:
            target_defines = f'{target}_defines'
            meson_content.append(f'{target_defines} = [')
            for define in defines:
                meson_content.append(f"\t'-D{define}',")
            meson_content.append(']')
            meson_content.append(f'{target_cpp_flags} += {target_defines}')

        target_include_paths = f'{target}_include_paths'
        meson_content.append(f'{target_include_paths} = include_directories(')
        include_paths = cpp.properties.get('include_paths')
        if include_paths:
            for include_path in include_paths:
                meson_content.append(f"\t'{include_path.path.as_posix()}',")
            meson_content.append(')')
        else:
            meson_content[-1] += ')'

        target_dependencies = f'{target}_dependencies'
        meson_content.append(f'{target_dependencies} = [')
        dependencies = cpp.properties.get('dependencies')
        if dependencies or cpp.is_python:
            for dependency in dependencies:
                meson_content.append(f'\t{dependency}_dep,')
            module_lib = cpp.properties.get('python_module_library', None)
            if module_lib:
                meson_content.append(f'\t{module_lib}_dep,')
            meson_content.append(']')
        else:
            meson_content[-1] += ']'

        if cpp.compiler_supports_property(cpp.compiler_flag, 'microsoft_crt'):
            from iprm.api.cpp import MicrosoftCRuntime
            crt = cpp.properties.get('microsoft_crt', MicrosoftCRuntime.DYNAMIC)
            if crt == MicrosoftCRuntime.DYNAMIC:
                meson_content.append("if get_option('buildtype') == 'debug'")
                meson_content.append(f"\t{target_cpp_flags} += ['/MDd']")
                meson_content.append("else")
                meson_content.append(f"\t{target_cpp_flags} += ['/MD']")
                meson_content.append("endif")
            elif crt == MicrosoftCRuntime.STATIC:
                meson_content.append("if get_option('buildtype') == 'debug'")
                meson_content.append(f"\t{target_cpp_flags} += ['/MTd']")
                meson_content.append("else")
                meson_content.append(f"\t{target_cpp_flags} += ['/MT']")
                meson_content.append("endif")

        if Env.platform.wasm:
            meson_content.append(f"{target_link_flags} += ['-s', 'MINIFY_HTML=0']")

        header_files = self._cpp_get_header_src_file_paths(cpp)
        source_files = self._cpp_get_source_src_file_paths(cpp)
        generated_source_files = []
        if cpp.is_qt:
            qt_library = cpp.properties.get('qt_library')
            with platform_context(Env.platform):
                qt_library_target = Session.get_object(qt_library)
                from iprm.api.cpp import QtThirdParty
                if qt_library_target.properties.get(QtThirdParty.MOC, False):
                    target_moc_headers = f'{target}_moc_headers'
                    meson_content.append(f'{target_moc_headers} = [')
                    if header_files:
                        for header_file in header_files:
                            meson_content.append(f'\t{header_file},')
                        meson_content.append(']')
                    else:
                        meson_content[-1] += ']'
                    header_files.clear()
                    target_moc_sources = f'{target}_moc_sources'
                    meson_content.append(f'{target_moc_sources} = iprm_moc_generator.process({target_moc_headers})')
                    generated_source_files.append(target_moc_headers)
                    generated_source_files.append(target_moc_sources)
                if qt_library_target.properties.get(QtThirdParty.RCC, False):
                    target_qrc_files = f'{target}_qrc_files'
                    qrc_files = self._cpp_get_sources(cpp, 'sources', ['qrc'], self.relative_src_path)
                    source_files = [file for file in source_files if file not in qrc_files]
                    meson_content.append(f'{target_qrc_files} = [')
                    if qrc_files:
                        for qrc_file in qrc_files:
                            meson_content.append(f'\t{qrc_file},')
                        meson_content.append(']')
                    else:
                        meson_content[-1] += ']'
                    target_qrc_sources = f'{target}_qrc_sources'
                    meson_content.append(f'{target_qrc_sources} = iprm_rcc_generator.process({target_qrc_files})')
                    generated_source_files.append(target_qrc_sources)
                if qt_library_target.properties.get(QtThirdParty.UIC, False):
                    target_ui_files = f'{target}_ui_files'
                    ui_files = self._cpp_get_sources(cpp, 'sources', ['ui'], self.relative_src_path)
                    source_files = [file for file in source_files if file not in ui_files]
                    meson_content.append(f'{target_ui_files} = [')
                    if ui_files:
                        for ui_file in ui_files:
                            meson_content.append(f'\t{ui_file},')
                        meson_content.append(']')
                    else:
                        meson_content[-1] += ']'
                    target_ui_sources = f'{target}_ui_sources'
                    meson_content.append(f'{target_ui_sources} = iprm_uic_generator.process({target_ui_files})')
                    generated_source_files.append(target_ui_sources)
                if qt_library_target.properties.get(QtThirdParty.CONF, False):
                    qt_conf_content = f"""{self._current_generated_file_header}
[Paths]
Prefix=@IPRM_QT_ROOT_DIR@
Plugins=@IPRM_QT_ROOT_DIR@/plugins
"""
                    qt_conf_template_file = self._current_generate_dir / 'qt.conf.in'
                    qt_conf_template_file.write_text(qt_conf_content)
                    meson_content.append('qt_conf_data = configuration_data()')
                    meson_content.append(
                        f"qt_conf_data.set('IPRM_QT_ROOT_DIR', meson.project_build_root() / '{qt_library_target.root_relative_dir.path.as_posix()}')")
                    meson_content.append('configure_file(')
                    meson_content.append("\tinput: 'qt.conf.in',")
                    meson_content.append("\toutput: 'qt.conf',")
                    meson_content.append("\tconfiguration: qt_conf_data,")
                    meson_content.append(')')

        if cpp.is_app or cpp.is_test:
            meson_content.append(f"{target} = executable('{target}',")
        elif cpp.is_static:
            meson_content.append(f"{target} = static_library('{target}',")
        elif cpp.is_shared:
            meson_content.append(f"{target} = shared_library('{target}',")
        elif cpp.is_python:
            meson_content.extend(self._generate_cpp_first_party_python_module(cpp))
        else:
            return meson_content

        for header_file in header_files:
            meson_content.append(f'\t{header_file},')
        for source_file in source_files:
            meson_content.append(f'\t{source_file},')
        for generated_files in generated_source_files:
            meson_content.append(f'\t{generated_files},')

        meson_content.append(f"\tcpp_args : {target_cpp_flags},")
        meson_content.append(f"\tinclude_directories : {target_include_paths},")
        meson_content.append(f"\tdependencies : {target_dependencies},")
        suffix = cpp.properties.get('suffix', '')
        if suffix:
            suffix = suffix[1:] if suffix.startswith('.') else suffix
            meson_content.append(f"\tname_suffix : '{suffix}',")

        if Env.platform.windows and cpp.is_app and cpp.is_gui:
            meson_content.append("\twin_subsystem : 'windows',")
            meson_content.append(f"\tlink_args : {target_link_flags} + ['/ENTRY:mainCRTStartup']")
        else:
            meson_content.append(f"\tlink_args : {target_link_flags}")
        meson_content.append(')')

        if not cpp.is_app and not cpp.is_test:
            target_dep = f'{target}_dep'
            if cpp.is_python:
                # CMake errors if we try to link directly with python modules as they are not static or shared
                # libraries, this is a workaround to ensure the shared_module is always built before it's dependency,
                # as Meson doesn't have any clean way to depend on a shared_module given we can't explicitly link it
                # with anything
                target_dep_impl = f'{target_dep}_impl'
                meson_content.append(f"{target_dep_impl} = custom_target(")
                meson_content.append(f"\t'{target_dep_impl}',")
                meson_content.append(f"\toutput: '{target_dep_impl}.txt',")
                meson_content.append(f"\tinput: {target},")
                meson_content.append(f"\tcommand: ['touch', '@OUTPUT@'],")
                meson_content.append(')')

                meson_content.append(f'{target_dep} = declare_dependency(')
                meson_content.append(f'\tsources: {target_dep_impl},')
                meson_content.append(')')
            else:
                meson_content.append(f'{target_dep} = declare_dependency(')
                meson_content.append(f"\tinclude_directories : {target_include_paths},")
                meson_content.append(f"\tlink_with : {target},")
                meson_content.append(')')

        if cpp.is_test:
            meson_content.append(f"test('{target}',")
            meson_content.append(f"\t{target},")
            meson_content.append(')')

        if cpp.is_shared:
            meson_content.append(f"{self.MESON_RUN_ENV}.prepend('PATH', {self.current_bin_dir()})")

        if cpp.is_app or cpp.is_test:
            run_target = f'run_{target}'
            meson_content.append(f"{run_target} = run_target('{run_target}',")
            if Env.platform.wasm:
                if suffix == 'html':
                    port = cpp.properties.get('server_port', 8080)
                    meson_content.extend(self._generate_cpp_wasm_html_run_target(target, port))
                else:
                    # TODO: If suffix is .js, execute the file with Node.js
                    pass
            else:
                meson_content.append(f'\tcommand: [{target}],')
            meson_content.append(f'\tdepends: [{target}],')
            meson_content.append(f'\tenv: {self.MESON_RUN_ENV},')
            meson_content.append(')')
        output_dir = cpp.properties.get('output_dir', None)
        if output_dir:
            raise NotImplementedError('Meson has not implemented custom build output directory')
        meson_content.extend(self._generate_target(cpp))
        meson_content.append('')
        return meson_content

    def _generate_cpp_first_party_python_module(self, cpp: CppTarget):
        meson_content = []
        target = cpp.name
        meson_content.append(f"{target} = shared_module('{target}',")
        return meson_content

    def _generate_cpp_wasm_html_run_target(self, target, port):
        meson_content = []
        meson_content.append('\tcommand: [')
        meson_content.append("\t\t'python', '-c',")
        meson_content.append(f"""'''{run_html_wasm_script(target)}
'''""")
        meson_content[-1] += ','
        meson_content.append(f"\t\t{target}.full_path(),")
        meson_content.append(f"\t\t'--port', '{port}'")
        meson_content.append('\t],')
        return meson_content

    def _generate_cpp_third_party(self, cpp: CppTarget):
        meson_content = []
        if cpp.is_source_archive:
            meson_content.extend(self._generate_cpp_third_party_source_archive(cpp))
        elif cpp.is_precompiled_archive:
            meson_content.extend(self._generate_cpp_third_party_precompiled_archive(cpp))
        elif cpp.is_imported:
            pass
        elif cpp.is_git:
            meson_content.extend(self._generate_cpp_third_party_git(cpp))
        return meson_content

    def _generate_cpp_third_party_source_archive(self, cpp: CppTarget):
        meson_content = self._add_archive_unpack_target(cpp)
        target = cpp.name
        target_dep = f'{target}_dep'

        target_include_paths = f'{target}_include_paths'
        include_paths = cpp.properties.get('include_paths')

        # TODO: Move this include dirs in binary dir workaround to a more general place as
        #  _generate_cpp_third_party_imported() needs the same thing
        meson_content.append(f'{target_include_paths} = [')
        if include_paths:
            for include_path in include_paths:
                meson_content.append(f"\t'{include_path.path.as_posix()}',")
            meson_content.append(']')
        else:
            meson_content[-1] += ']'

        meson_content.append(f'foreach path : {target_include_paths}')
        meson_content.append(f'\tbuild_dir_path = {self.current_bin_dir()} / path')
        meson_content.append(
            f"\trun_command('python', '-c', 'import sys; import os; os.makedirs(sys.argv[1], exist_ok=True)', build_dir_path, check: true)")
        meson_content.append('endforeach')

        meson_content.append(f'{target_include_paths} = include_directories(')
        if include_paths:
            for include_path in include_paths:
                meson_content.append(f"\t'{include_path.path.as_posix()}',")
            meson_content.append(')')
        else:
            meson_content[-1] += ')'

        unpack_target_name_dep = f"{cpp.properties.get('unpack_target_name')}_dep"
        if cpp.is_header:
            meson_content.append(f'{target_dep} = declare_dependency(')
            meson_content.append(f"\tinclude_directories : {target_include_paths},")
            meson_content.append(f'\tdependencies: [{unpack_target_name_dep}]')
            meson_content.append(')')
            meson_content.append('')
        else:
            # TODO: I haven't figured out how to get source archive generation working smoothly for Meson yet, CMake
            #  has built in and very clean support for this, but it seems much more complex to get right with Meson.
            #  In particular, telling Meson that files that are going to be unpacked don't exist yet. Potential solution
            #  here is a generator(), but Meson itself says that that is not really what they are supposed to be used
            #  for and a custom_target should be used instead. The real roadblock is that Meson is very strict and very opinionated and
            #  doesn't let you specify paths as output for custom targets, it assumes the content is going directly in
            #  the root build dir, but that is not true for the unpacked content, as it can be extracted into any
            #  arbitrary level of folder depth. So for now I'm throwing in the towel here, and thankful that CMake
            #  doesn't get in your way and lets you do easy/obvious things in an easy/obvious way. This should get done
            #  eventually though, and maybe it is easy for a Meson expert to implement.
            raise NotImplementedError('Meson backend does not currently support a source archive target that needs to '
                                      'compile the unpacked sources directly')
        return meson_content

    def _generate_cpp_third_party_precompiled_archive(self, cpp: CppTarget):
        meson_content = self._add_archive_unpack_target(cpp)

        # NOTE: Meson is stricter about the order of targets/dependency objects. Because of this, imported targets
        # can't generate themselves, but the actual explicit target the user created that implicitly created all the
        # modules from the builder needs to also be responsible for generation
        unpack_target_name = cpp.properties.get('unpack_target_name')
        dependencies = cpp.dependencies
        with platform_context(Env.platform):
            for dependency in dependencies:
                dep_target = Session.get_object(dependency)
                if dep_target.is_cpp and dep_target.is_imported and dep_target.properties.get('unpack_target_name',
                                                                                              '') == unpack_target_name:
                    cpp_dep_target = cast(CppTarget, dep_target)
                    meson_content.extend(self._generate_cpp_third_party_imported(cpp_dep_target))

        target = cpp.name
        target_dep = f'{target}_dep'
        meson_content.append(f'{target_dep} = declare_dependency(')
        if dependencies:
            meson_content.append('\tdependencies: [')
            for dependency in dependencies:
                meson_content.append(f'\t\t{dependency}_dep,')
            meson_content.append('\t],')
            meson_content.append(')')
        meson_content.append('')

        if cpp.is_qt:
            meson_content.extend(self._generate_cpp_qt_third_party_precompiled_archive(cpp, unpack_target_name))

        meson_content.append('')
        return meson_content

    def _generate_cpp_qt_third_party_precompiled_archive(self, cpp: CppTarget, unpack_target_name: str):
        meson_content = []
        # TODO: move this into its own _generate_cpp_qt_third_party_precompiled_archive function (for CMake too) as
        #  each known third party lib will have this behaviour
        qt_utils_file_path = self._current_generate_dir / 'meson_qt_utils.py'
        with qt_utils_file_path.open(mode='a') as qt_utils_file:
            qt_utils_file.write(f"""{self._current_generated_file_header}
import os
import sys
import subprocess

# First argument is the absolute path to the executable
if len(sys.argv) < 2:
    print("Usage: wrapper.py <executable_path> [arguments...]")
    sys.exit(1)

executable_path = sys.argv[1]
args = sys.argv[2:]

# Check if Qt directory exists
qt_bin_dir = os.path.dirname(executable_path)
if not os.path.exists(qt_bin_dir):
    print(f"Error: Qt binary directory '{{qt_bin_dir}}' does not exist")
    sys.exit(1)

# Forward all remaining arguments to the actual executable
cmd = [executable_path] + args
try:
    result = subprocess.run(cmd)
    sys.exit(result.returncode)
except FileNotFoundError:
    print(f"Error: Executable '{{executable_path}}' not found")
    sys.exit(1)
""")
        meson_content.append(f"meson_qt_utils = {self.current_src_dir()} / 'meson_qt_utils.py'")
        meson_content.append(
            f"iprm_qt_root_dir = meson.project_build_root() / '{cpp.root_relative_dir.path.as_posix()}'")
        meson_content.append(f"iprm_qt_bin_dir = iprm_qt_root_dir / '{cpp.properties.get('bin_dir').path.as_posix()}'")
        meson_content.append(f"{self.MESON_RUN_ENV}.prepend('PATH', iprm_qt_bin_dir)")
        meson_content.append(f"iprm_qt_moc = iprm_qt_bin_dir / '{QtThirdParty.MOC}'")
        meson_content.append(f"""iprm_moc_generator = generator(
  python,
  output: 'moc_@BASENAME@.cpp',
  arguments: [meson_qt_utils, iprm_qt_moc, '@INPUT@', '-o', '@OUTPUT@'],
  depends: [{unpack_target_name}],
)
""")
        meson_content.append(f"iprm_qt_rcc = iprm_qt_bin_dir / '{QtThirdParty.RCC}'")
        meson_content.append(f"""iprm_rcc_generator = generator(
  python,
  output: 'qrc_@BASENAME@.cpp',
  arguments: [meson_qt_utils, iprm_qt_rcc, '@INPUT@', '-o', '@OUTPUT@'],
  depends: [{unpack_target_name}],
)
""")
        meson_content.append(f"iprm_qt_uic = iprm_qt_bin_dir / '{QtThirdParty.UIC}'")
        meson_content.append(f"""iprm_uic_generator = generator(
  python,
  output: 'ui_@BASENAME@.h',
  arguments: [meson_qt_utils, iprm_qt_uic, '@INPUT@', '-o', '@OUTPUT@'],
  depends: [{unpack_target_name}],
)
""")
        return meson_content

    @classmethod
    def _add_archive_unpack_target(cls, cpp: CppTarget):
        unpack_target_name = cpp.properties.get('unpack_target_name')
        archive_dir = cpp.properties.get('archive_dir')
        archive_file = cpp.properties.get('archive_file')
        archive_file_path = cls.relative_src_path(archive_dir, archive_file)
        meson_content = [
            "python = import('python').find_installation(required: true)",
            f'{unpack_target_name} = custom_target(',
            f"\t'{unpack_target_name}',",
            f'\tinput: {archive_file_path},',
        ]

        meson_content.append('\toutput: [')
        meson_content.append(f"\t\t'{unpack_target_name}.sentinel',")
        meson_content.append('\t],')
        meson_content.append('\tcommand: [')
        meson_content.append("\t\tpython, '-c',")
        meson_content.append("""'''import sys, os, zipfile, tarfile
archive_file = sys.argv[1]
sentinel_file = sys.argv[2]
build_dir = os.path.dirname(sentinel_file)
if archive_file.endswith('.zip'):
	with zipfile.ZipFile(archive_file, 'r') as zip_ref:
		zip_ref.extractall(build_dir)
elif archive_file.endswith('.tar.gz'):
	with tarfile.open(archive_file, 'r') as tar_ref:
		tar_ref.extractall(build_dir)
open(sentinel_file, 'w').close()
'''"""
                             )
        meson_content[-1] += ','
        meson_content.append("\t\t'@INPUT@',")
        meson_content.append("\t\t'@OUTPUT@',")
        meson_content.append('\t],')
        meson_content.append(')')

        unpack_target_dep = f'{unpack_target_name}_dep'
        meson_content.append(f'{unpack_target_dep} = declare_dependency(')
        meson_content.append(f'\tsources: {unpack_target_name}')
        meson_content.append(')')
        meson_content.append('')
        return meson_content

    def _generate_cpp_third_party_imported(self, cpp: CppTarget):
        meson_content = []
        # NOTE: Nothing to do here for executables in as far as I can tell
        if not cpp.is_lib:
            return meson_content
        target = cpp.name

        # Meson is very annoying and odd about include paths, even worse than CMake is for this scenario. For some
        # reason Meson forces a relative path structure for include paths. It errors at configure time if you try to
        # use absolute paths, even when you use their own built-in path helpers. See
        # https://github.com/mesonbuild/meson/issues/1535#issuecomment-289758714 for the summary: They evaluate at
        # both the current binary root and the current source root implicitly, and it must exist at least one of them
        # at configure time to be used in an include_directories() call
        target_include_paths = f'{target}_include_paths'
        include_paths = cpp.properties.get('include_paths', [])

        meson_content.append(f'{target_include_paths} = [')
        if include_paths:
            for include_path in include_paths:
                meson_content.append(f"\t'{include_path.path.as_posix()}',")
            meson_content.append(']')
        else:
            meson_content[-1] += ']'

        meson_content.append(f'foreach path : {target_include_paths}')
        meson_content.append(f'\tbuild_dir_path = {self.current_bin_dir()} / path')
        meson_content.append(
            f"\trun_command('python', '-c', 'import sys; import os; os.makedirs(sys.argv[1], exist_ok=True)', build_dir_path, check: true)")
        meson_content.append('endforeach')

        meson_content.append(f'{target_include_paths} = include_directories(')
        if include_paths:
            for include_path in include_paths:
                meson_content.append(f"\t'{include_path.path.as_posix()}',")
            meson_content.append(')')
        else:
            meson_content[-1] += ')'

        imported = cpp.properties.get('imported')
        bin_dir = imported.get('bin_dir')
        bin_debug = self.relative_bin_path(bin_dir, imported.get('debug_bin_file'))
        bin_release = self.relative_bin_path(bin_dir, imported.get('release_bin_file'))
        implib_dir = imported.get('implib_dir', None)
        implib_debug = self.relative_bin_path(implib_dir, imported.get('debug_implib_file')) if implib_dir else None
        implib_release = self.relative_bin_path(implib_dir, imported.get('release_implib_file')) if implib_dir else None

        meson_content.append("if get_option('buildtype') == 'debug'")

        target_libraries = f'{target}_libraries'
        meson_content.append(f'{target_libraries} = [')
        if implib_debug and Env.platform.windows:
            meson_content.append(f'\t{implib_debug},')
        else:
            meson_content.append(f'\t{bin_debug},')
        meson_content.append(']')

        meson_content.append("else")

        target_libraries = f'{target}_libraries'
        meson_content.append(f'{target_libraries} = [')
        if implib_release and Env.platform.windows:
            meson_content.append(f'\t{implib_release},')
        else:
            meson_content.append(f'\t{bin_release},')
        meson_content.append(']')

        meson_content.append("endif")

        unpack_target_name = cpp.properties.get('unpack_target_name', None)
        target_dep = f'{target}_dep'
        meson_content.append(f'{target_dep} = declare_dependency(')
        meson_content.append('\tdependencies: [')
        meson_content.append(f'\t\t{unpack_target_name}_dep,')
        meson_content.append('\t],')
        meson_content.append(f"\tinclude_directories : {target_include_paths},")
        meson_content.append(f"\tlink_args : {target_libraries},")
        meson_content.append(')')
        meson_content.append('')
        return meson_content

    def _generate_cpp_third_party_git(self, cpp: CppTarget):
        # TODO: Make this happen at build time and use dependency clone marker for dependent libs
        meson_content = []
        target = cpp.name
        target_type_name = type(cpp).__name__
        repository = cpp.properties.get('git_repository')
        tag = cpp.properties.get('git_tag')
        # TODO: For now just hardcode to only support the latest version, but in the future we should at least
        #  support all WrapDB's for a third party git content source we expose on the API
        if target_type_name == 'GTestThirdParty' and tag == 'v1.15.2':
            # See https://mesonbuild.com/Wrapdb-projects.html for supported gtest versions
            gtest_dbwrap = self._meson_subprojects_dir / 'gtest.wrap'
            gtest_dbwrap.write_text(f"""{self._current_generated_file_header}
[wrap-file]
directory = googletest-1.15.2
source_url = https://github.com/google/googletest/archive/refs/tags/v1.15.2.tar.gz
source_filename = gtest-1.15.2.tar.gz
source_hash = 7b42b4d6ed48810c5362c265a17faebe90dc2373c885e5216439d37927f02926
patch_filename = gtest_1.15.2-4_patch.zip
patch_url = https://wrapdb.mesonbuild.com/v2/gtest_1.15.2-4/get_patch
patch_hash = a5151324b97e6a98fa7a0e8095523e6d5c4bb3431210d6ac4ad9800c345acf40
source_fallback_url = https://github.com/mesonbuild/wrapdb/releases/download/gtest_1.15.2-4/gtest-1.15.2.tar.gz
wrapdb_version = 1.15.2-4

[provide]
gtest = gtest_dep
gtest_main = gtest_main_dep
gmock = gmock_dep
gmock_main = gmock_main_dep 
""")
            meson_content.append(f"{target} = subproject('gtest')")
            meson_content.append(f"{target}_dep = declare_dependency(")
            meson_content.append('\tdependencies: [')
            meson_content.append(f"\t\t{target}.get_variable('gtest_dep'),")
            meson_content.append(f"\t\t{target}.get_variable('gmock_dep'),")
            meson_content.append('\t],')
            meson_content.append(')')
            meson_content.append('')
        elif target_type_name == 'PyBind11ThirdParty' and tag == 'v2.13.5':
            pybind11_dbwrap = self._meson_subprojects_dir / 'pybind11.wrap'
            pybind11_dbwrap.write_text(f"""{self._current_generated_file_header}
[wrap-file]
directory = pybind11-2.13.5
source_url = https://github.com/pybind/pybind11/archive/refs/tags/v2.13.5.tar.gz
source_filename = pybind11-2.13.5.tar.gz
source_hash = b1e209c42b3a9ed74da3e0b25a4f4cd478d89d5efbb48f04b277df427faf6252
patch_filename = pybind11_2.13.5-1_patch.zip
patch_url = https://wrapdb.mesonbuild.com/v2/pybind11_2.13.5-1/get_patch
patch_hash = ecb031b830481560b3d8487ed63ba4f5509a074be42f5d19af64d844c795e15b
source_fallback_url = https://github.com/mesonbuild/wrapdb/releases/download/pybind11_2.13.5-1/pybind11-2.13.5.tar.gz
wrapdb_version = 2.13.5-1

[provide]
pybind11 = pybind11_dep
""")
            # TODO: This most likely isn't working correctly on non Windows platforms wrt linking with python
            meson_content.append(f"{target} = subproject('pybind11')")
            meson_content.append("python = import('python').find_installation(required: true)")
            meson_content.append("py_include_dir = python.get_path('include')")
            target_include_directories = f'{target}_include_directories'
            meson_content.append(f'{target_include_directories} =  include_directories(')
            meson_content.append("\tpy_include_dir,")
            meson_content.append(')')
            target_dependencies = f'{target}_dependencies'
            meson_content.append(f'{target_dependencies} = [')
            meson_content.append(f"\t{target}.get_variable('pybind11_dep'),")
            meson_content.append(']')
            meson_content.append("if host_machine.system() == 'windows'")
            meson_content.append("\tbase_dir = py_include_dir.split('Include')[0]")
            meson_content.append("\tpython_lib_dir = base_dir + 'libs'")
            meson_content.append(
                "\tpy_version_cmd = run_command(python, '-c', 'import sys; print(str(sys.version_info[0]) + str(sys.version_info[1]))', check: true)")
            meson_content.append("\tpython_lib_name = 'python' + py_version_cmd.stdout().strip()")
            meson_content.append("\tcpp = meson.get_compiler('cpp')")
            meson_content.append(
                '\tpython_lib = cpp.find_library(python_lib_name, dirs: [python_lib_dir], required: true)')
            meson_content.append(f'\t{target_dependencies} += python_lib')
            meson_content.append('endif')
            meson_content.append(f"{target}_dep = declare_dependency(")
            meson_content.append(f'\tinclude_directories: {target_include_directories},')
            meson_content.append(f'\tdependencies: {target_dependencies},')
            meson_content.append(')')
            meson_content.append('')
        return meson_content

    @classmethod
    def _cpp_add_sources(cls, cpp: CppTarget, key: str):
        meson_content_sources = []
        sources_dict = cpp.properties.get(key, {})
        if sources_dict:
            for src_dir, src_files in sources_dict.items():
                for src_file in src_files:
                    meson_content_sources.append(f"\t{cls.relative_src_path(src_dir, src_file)},")
        return meson_content_sources

    def _generate_rust(self, rust: RustTarget):
        if not rust.compiler_supports_property(rust.compiler_flag, 'crate'):
            return []
        target = rust.name
        manifest_dir, cargo_file = rust.properties.get('manifest')
        manifest_file = self.relative_src_path(manifest_dir, cargo_file)

        meson_inputs_content = '\tinput: files(\n'
        meson_inputs_content += f'\t\t{manifest_file},\n'
        sources_dict = rust.properties.get('sources', {})
        if sources_dict:
            for src_dir, src_files in sources_dict.items():
                for src_file in src_files:
                    meson_inputs_content += f"\t\t{self.relative_src_path(src_dir, src_file)},\n"
        meson_inputs_content += '\t),'

        meson_content = [
            "cargo_profile = 'dev'",
            "if get_option('buildtype') == 'release' or get_option('buildtype') == 'minsize'",
            "\tcargo_profile = 'release'",
            "endif",
            "",
            f"custom_target('{target}',",
            meson_inputs_content,
            f"\toutput : '{target}',",
            "\tconsole : true,",
            "\tcommand : [",
            "\t\tfind_program('cargo'),",
            "\t\t'build',",
            f"\t\t'--manifest-path', {manifest_file},",
            "\t\t'--target-dir', meson.current_build_dir(),",
            "\t\t'--profile', cargo_profile,",
        ]
        cargo_locked = rust.properties.get('cargo_locked', False)
        if cargo_locked:
            meson_content.append("\t\t'--locked'")
        meson_content.append("\t],")
        meson_content.append(")")
        meson_content.append('')
        return meson_content
