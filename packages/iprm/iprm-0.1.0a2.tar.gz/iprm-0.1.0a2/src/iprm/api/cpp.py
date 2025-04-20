"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from enum import IntEnum
from iprm.api.target import Target
from iprm.core.typeflags import (CPP, PYTHON, STATIC, SHARED, EXECUTABLE, TEST, HEADER, GUI, THIRDPARTY, IMPORTED,
                                 PKGCONFIG, ARCHIVE, PRECOMPILED, SOURCE, GIT, VCPKG, CONAN, HOMEBREW, SYSTEM, DPKG,
                                 RPM, QT, MSVC, CLANG, GCC, EMSCRIPTEN)
from iprm.util.dir import Dir, BinaryDir
from iprm.util.env import Env
from iprm.util.platform import windows, macos, linux
from iprm.util.compiler import MSVC_COMPILER_NAME, CLANG_COMPILER_NAME, GCC_COMPILER_NAME, EMSCRIPTEN_COMPILER_NAME, \
    msvc, clang, gcc, emscripten
from iprm.api.builder import SourceArchiveBuilder, PrecompiledArchiveBuilder, GitBuilder


class MicrosoftCRuntime(IntEnum):
    STATIC = 1
    DYNAMIC = 2


class CppTarget(Target):
    STANDARD = 'standard'
    CONFORMANCE = 'conformance'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= CPP
        self.hex_colour = '#3388CC'
        self.properties['headers']: dict[Dir, list[str]] = {}
        self.properties['sources']: dict[Dir, list[str]] = {}
        self.properties['libraries']: list[str] = []
        self.properties['patches']: dict[Dir, list[str]] = {}
        self.properties['defines']: list[str] = []
        self.properties['include_paths']: list[Dir] = []
        self.properties['runtime_files']: dict[Dir, list[str]] = {}
        self.properties['runtime_paths']: list[Dir] = []
        self._compiler_flag = CppTarget.default_compiler_flag()

    @classmethod
    def default_compiler_flag(cls):
        if Env.platform.windows:
            return MSVC
        elif Env.platform.macos:
            return CLANG
        elif Env.platform.linux:
            return GCC
        elif Env.platform.wasm:
            return EMSCRIPTEN
        return None

    @classmethod
    def default_compiler_name(cls):
        if Env.platform.windows:
            return MSVC_COMPILER_NAME
        elif Env.platform.macos:
            return CLANG_COMPILER_NAME
        elif Env.platform.linux:
            return GCC_COMPILER_NAME
        elif Env.platform.wasm:
            return EMSCRIPTEN_COMPILER_NAME
        return None

    @classmethod
    def default_language_properties(cls, **kwargs):
        defaults = {
            cls.STANDARD: '20',
            cls.CONFORMANCE: True,
        }
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        return kwargs

    @property
    def compiler_flag(self):
        return self._compiler_flag

    @compiler_flag.setter
    def compiler_flag(self, flag):
        self._compiler_flag = flag

    def headers(self, header_dir: Dir, *headers):
        if header_dir not in self.properties['headers']:
            self.properties['headers'][header_dir] = []
        self.properties['headers'][header_dir].extend(headers)

    def sources(self, src_dir: Dir, *sources):
        if src_dir not in self.properties['sources']:
            self.properties['sources'][src_dir] = []
        self.properties['sources'][src_dir].extend(sources)

    # TODO: Don't assume the lirbaries are on the path or available at the system/compiler level. 
    #  Add a lib_dir parameter to ahndle this
    def libraries(self, *libraries):
        self.properties['libraries'].extend(libraries)

    # TODO: allow to explicitly declare if the defines or include paths are transitive (i.e. targets that
    #  depend on this target will implicitly get these too) or if they are private and only relevant to this target.
    #  Since they can be called multiple times, you can have sets of each property that are transitive, and sets that
    #  aren't

    def defines(self, *defines):
        self.properties['defines'].extend(defines)

    def include_paths(self, *paths: tuple[Dir]):
        self.properties['include_paths'].extend(paths)

    def patches(self, patch_dir: Dir, *patches):
        if patch_dir not in self.properties['patches']:
            self.properties['patches'][patch_dir] = []
        self.properties['patches'][patch_dir].extend(patches)

    def runtime_files(self, files_dir: Dir, *files):
        if files_dir not in self.properties['runtime_files']:
            self.properties['runtime_files'][files_dir] = []
        self.properties['runtime_files'][files_dir].extend(files)

    def runtime_paths(self, *paths: tuple[Dir]):
        self.properties['runtime_paths'].extend(paths)

    def static_crt(self):
        self.microsoft_crt(MicrosoftCRuntime.STATIC)

    def dynamic_crt(self):
        self.microsoft_crt(MicrosoftCRuntime.DYNAMIC)

    @msvc
    def microsoft_crt(self, crt: MicrosoftCRuntime):
        self.properties['microsoft_crt'] = crt

    def imported(self, **kwargs):
        self.properties['imported'] = kwargs

    def output_dir(self, output_dir: Dir):
        self.properties['output_dir'] = output_dir

    def qt(self, qt_lib: str):
        self.properties['qt_library'] = qt_lib
        self.requires(qt_lib, )
        self.type_flags |= QT

    def header(self):
        self.type_flags |= HEADER

    def executable(self):
        self.type_flags |= EXECUTABLE

    def static(self):
        self.type_flags |= STATIC

    def shared(self):
        self.type_flags |= SHARED

    def test(self):
        self.type_flags |= TEST

    def python(self):
        self.type_flags |= PYTHON


class CppExecutable(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diamond()
        self.executable()

    def gui(self):
        self.type_flags |= GUI


class CppStaticLibrary(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ellipse()
        self.static()


class CppSharedLibrary(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ellipse()
        self.shared()


class CppTest(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diamond()
        self.test()


class CppPythonModule(CppTarget):
    def __init__(self, *args, **kwargs):
        py_maj = kwargs.pop('maj')
        py_min = kwargs.pop('min')
        py_mod_lib = kwargs.pop('mod_lib')
        super().__init__(*args, **kwargs)
        self.properties['python_version_major'] = py_maj
        self.properties['python_version_minor'] = py_min
        self.properties['python_module_library'] = py_mod_lib
        self.requires(py_mod_lib, )
        self.suffix(self._get_py_module_suffix())
        self.python()

    @staticmethod
    def _get_py_module_suffix():
        import sysconfig
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        if ext_suffix:
            return ext_suffix
        return None


class CppThirdParty(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= THIRDPARTY

    # TODO: expose an icon() method so third party libraries specify their icon path that way instead of
    #  hardcoding into the IPRM Studio's AssetCache, making things much more extensible

    def source_archive(self, archive_dir: Dir, archive_file: str):
        self.type_flags |= (ARCHIVE | SOURCE)
        return SourceArchiveBuilder(self, archive_dir, archive_file)

    def precompiled_archive(self, archive_dir: Dir, archive_file: str):
        self.type_flags |= (ARCHIVE | PRECOMPILED)
        return PrecompiledArchiveBuilder(self, archive_dir, archive_file)

    def git(self):
        self.type_flags |= GIT
        return GitBuilder(self)

    def vcpkg(self, manifest_dir: Dir):
        # TODO: specify required vcpkg stuff here, ensure to only support the latest/modern way of doing things (I
        #  think that is some manifest stuff?)
        # TODO: For now, actually just make vcpkg (and probably conan too) a project wide thing, where one maps their
        #  names to targets (that will be ContainerTarget's) that first party targets can then depend on
        self.type_flags |= VCPKG
        self.properties['manifest'] = manifest_dir,

    def conan(self):
        # TODO: specify required conan stuff here
        self.type_flags |= CONAN

    @macos
    @linux
    def homebrew(self, **kwargs):
        self.type_flags |= HOMEBREW
        package = kwargs.get('package')
        self.properties['homebrew_package'] = package
        libs = kwargs.get('shared_libs')
        for lib in libs:
            lib_target_name = f'{self.name}_{lib}'
            brew_target_name = f'{self.name}_brew'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | HOMEBREW | IMPORTED)
            lib_target.properties['homebrew_lib'] = lib
            lib_target.properties['homebrew_target'] = brew_target_name
            self.requires(lib_target_name, )
        self.properties['homebrew_libs'] = libs

    # TODO: Technically Windows supports pkg-config, but keep going to keep it to unix only for now
    @macos
    @linux
    def pkgconfig(self, **kwargs):
        # TODO: Some backend (e.g. CMake AND Meson) have native support for this, so this impl will be relatively clean
        # NOTE: Use the freedesktop.svg logo for this int he target properties view
        # NOTE: Windows technically supports this too, when adding tests for it, ensure it is something simple that can
        # be easily done on all platforms, or if not create platform-specific versions of the target that rely on
        # basic/simple packages each platform always has available by default
        self.type_flags |= PKGCONFIG
        prefix = kwargs.get('prefix', None)
        libs = kwargs.get('shared_libs')
        modules = []
        imported_targets = []
        for lib in libs:
            module = lib.removeprefix(prefix) if prefix else lib
            modules.append(module)
            lib_target_name = f'{self.name}_{module}'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | PKGCONFIG | IMPORTED)
            lib_target.properties['pkconfig_module'] = f'{self.name.upper()}_{module.upper()}'
            lib_target.properties['pkconfig_lib'] = lib
            self.requires(lib_target_name, )
            imported_targets.append(lib_target)
        self.properties['pkconfig_modules'] = modules
        return imported_targets

    @linux
    def dpkg(self, **kwargs):
        self.type_flags |= (SYSTEM | DPKG)
        self.properties['dpkg_package'] = kwargs.get('package')

    def rpm(self, **kwargs):
        self.type_flags |= (SYSTEM | RPM)
        self.properties['rpm_package'] = kwargs.get('package')


# TODO: Move Qt out of builtin objects into the plugin objects API. GIven the extra generation complexity required
#  for moc/rcc/uic, we need a "generator" plugin that allows for external generation of content for a given object
#  and backend. Another library that would need this before it can be a plugin is protobuf

class QtPrecompiledArchiveBuilder(PrecompiledArchiveBuilder):
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target, archive_dir, archive_file)
        self._modules: list[str] = []
        self._lib_type: str = ''

    def shared_lib_pattern(self, **kwargs):
        super()._lib_pattern(**kwargs)
        self._lib_type = 'shared'

    def static_lib_pattern(self, **kwargs):
        super()._lib_pattern(**kwargs)
        self._lib_type = 'static'

    # TODO: Add ability to customize the actual module name for each Qt core in case of custom Qt build that deviates
    #  from Qts naming conventions here

    def core(self):
        self._module('Core')

    def network(self):
        self._module('Network')

    def gui(self):
        self._module('Gui')

    def widgets(self):
        self._module('Widgets')

    def svg(self):
        self._module('Svg')

    def svgwidgets(self):
        self._module('SvgWidgets')

    # TODO: Add remaining modules when needed

    def _module(self, name):
        if self._lib_type == 'shared':
            self._shared_pattern_libraries.append(name)
        elif self._lib_type == 'static':
            self._static_pattern_libraries.append(name)

    def tools(self, **kwargs):
        if kwargs.get('moc', False):
            self._auxiliary_apps.append(f'moc{self.app_suffix()}')
        if kwargs.get('rcc', False):
            self._auxiliary_apps.append(f'rcc{self.app_suffix()}')
        if kwargs.get('uic', False):
            self._auxiliary_apps.append(f'uic{self.app_suffix()}')

    def build(self):
        targets = super().build()
        for target in targets:
            target.type_flags |= QT
            target.hex_colour = '#41CD52'
            target.rectangle()
        self._target.properties['bin_dir'] = self._bin_dir
        return targets


class QtThirdParty(CppThirdParty):
    MOC = 'moc'
    RCC = 'rcc'
    UIC = 'uic'
    CONF = 'conf'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= QT
        self.hex_colour = '#41CD52'

    @macos
    @linux
    def pkgconfig(self, **kwargs):
        imported_targets = super().pkgconfig(**kwargs)
        for target in imported_targets:
            target.type_flags |= QT
            target.hex_colour = self.hex_colour
        return imported_targets

    def precompiled_archive(self, archive_dir: Dir, archive_file: str):
        self.type_flags |= (ARCHIVE | PRECOMPILED)
        return QtPrecompiledArchiveBuilder(self, archive_dir, archive_file)

    def moc(self):
        self.properties[QtThirdParty.MOC] = True

    def rcc(self):
        self.properties[QtThirdParty.RCC] = True

    def uic(self):
        self.properties[QtThirdParty.UIC] = True

    def conf(self):
        self.properties[QtThirdParty.CONF] = True
