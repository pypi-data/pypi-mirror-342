"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""

from typing import Optional
from abc import ABC, abstractmethod
from pathlib import Path

from iprm.util.env import Env
from iprm.core.typeflags import THIRDPARTY, ARCHIVE, PRECOMPILED, IMPORTED
from iprm.util.dir import Dir, RootRelativeBinaryDir


class Builder(ABC):
    def __init__(self, third_party_target):
        from iprm.api.cpp import CppThirdParty
        self._target: CppThirdParty = third_party_target

    @abstractmethod
    def build(self):
        pass


class ArchiveBuilder(Builder):
    # TODO: provide a way to specify the archive needs to be fetched from a remote location.
    #  To implement this, just allow for this to be initialized with a URL instead of a local directory. The builder
    #  will also expose methods for user specifying authentication as well if required.
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target)
        self._target.properties['archive_dir'] = archive_dir
        self._target.properties['archive_file'] = archive_file
        self._unpack_target_name = f'{self._target.name}_unpack'
        self._unpack_artifacts: list[dict[str, str]] = []

    def build(self):
        self._target.properties['unpack_target_name'] = self._unpack_target_name
        self._target.properties['unpack_artifacts'] = self._unpack_artifacts


class SourceArchiveBuilder(ArchiveBuilder):
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target, archive_dir, archive_file)

    def headers(self, header_dir: Dir, *headers):
        self._target.headers(header_dir, *headers)

    def sources(self, src_dir: Dir, *sources):
        self._target.sources(src_dir, *sources)

    def patches(self, patch_dir: Dir, *patches):
        self._target.patches(patch_dir, *patches)

    def static_crt(self):
        self._target.static_crt()

    def dynamic_crt(self):
        self._target.dynamic_crt()

    def include_paths(self, *paths: tuple[Dir]):
        self._target.include_paths(*paths)

    def header(self):
        self._target.header()

    def executable(self):
        self._target.executable()

    def static(self):
        self._target.static()

    def shared(self):
        self._target.shared()

    def qt(self, qt_lib: str):
        self._target.qt(qt_lib)


class PrecompiledArchiveBuilder(ArchiveBuilder):
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target, archive_dir, archive_file)
        self._include_dir: Optional[Dir] = None
        self._implib_dir: Optional[Dir] = None
        self._lib_dir: Optional[Dir] = None
        self._bin_dir: Optional[Dir] = None
        self._shared_pattern_libraries: list[str] = []
        self._shared_libraries: list[str] = []
        self._static_pattern_libraries: list[str] = []
        self._static_libraries: list[str] = []
        self._include_pattern: Optional[Dir] = None
        self._release_pattern: Optional[str] = None
        self._debug_pattern: Optional[str] = None
        from iprm.api.cpp import CppStaticLibrary, CppSharedLibrary
        self._shared_lib_targets: list[CppSharedLibrary] = []
        self._static_lib_targets: list[CppStaticLibrary] = []
        self._auxiliary_apps: list[str] = []

    def include_dir(self, include_dir: Dir):
        self._include_dir = include_dir

    def implib_dir(self, implib_dir: Dir):
        self._implib_dir = implib_dir

    def lib_dir(self, lib_dir: Dir):
        self._lib_dir = lib_dir

    def bin_dir(self, bin_dir: Dir):
        self._bin_dir = bin_dir

    def shared_libs(self, *modules):
        self._shared_libraries.extend(modules)

    def shared_lib_pattern(self, **kwargs):
        self._shared_pattern_libraries.extend(kwargs.get('modules'))
        self._lib_pattern(**kwargs)

    # TODO: Support static_lib_pattern
    """
    def static_lib_pattern(self, **kwargs):
        self._static_pattern_libraries.extend(kwargs.get('modules'))
        self._lib_pattern(**kwargs)
    """

    def _lib_pattern(self, **kwargs):
        self._include_pattern = kwargs.get('include', None)
        self._release_pattern = kwargs.get('release')
        self._debug_pattern = kwargs.get('debug')

    # TODO: Add static_lib_explicit

    # TODO: For now these are implicitly relative to the bin dir, but we should allow for specifying apps that are in
    #  sub folders etc and remove this assumption
    def auxiliary_apps(self, *apps):
        self._auxiliary_apps.extend(apps)

    def build(self):
        from iprm.api.cpp import CppStaticLibrary, CppSharedLibrary
        pattern_lib_names = self._shared_pattern_libraries
        for lib_name in pattern_lib_names:
            lib_target_name = f'{self._target.name}_{lib_name}'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | ARCHIVE | PRECOMPILED)
            lib_target.properties['unpack_target_name'] = self._unpack_target_name
            if self._include_pattern:
                dir_type = self._include_pattern.__class__
                lib_include_path = str(self._include_pattern.path)
                lib_include_path = lib_include_path.replace('%module%', lib_name)
                include_dir = dir_type(Path(lib_include_path))
                lib_target.include_paths(include_dir, )

            # TODO: Allow for the bin and implib names to have their own patterns (required for official
            #  precompiled ICU)
            lib_release_name = self._release_pattern.replace('%module%', lib_name)
            lib_debug_name = self._debug_pattern.replace('%module%', lib_name)
            bin_suffix = self._shared_lib_suffix()
            bin_suffix = '' if bin_suffix is None else bin_suffix
            imported_kwargs = {
                'lib_dir': self._lib_dir,
                'release_lib_file': f'{lib_release_name}{bin_suffix}',
                'debug_lib_file': f'{lib_debug_name}{bin_suffix}',
            }
            if self._implib_dir:
                imported_kwargs['implib_dir'] = self._implib_dir
                imported_kwargs['release_implib_file'] = f'{lib_release_name}.lib'
                imported_kwargs['debug_implib_file'] = f'{lib_debug_name}.lib'

            lib_target.type_flags |= IMPORTED
            lib_target.imported(**imported_kwargs)
            self._unpack_artifacts.append(imported_kwargs)
            self._target.requires(lib_target_name, )
            self._shared_lib_targets.append(lib_target)

        lib_names = self._shared_libraries
        for lib_name in lib_names:
            lib_target_name = f'{self._target.name}_{lib_name}'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | ARCHIVE | PRECOMPILED)
            lib_target.properties['unpack_target_name'] = self._unpack_target_name

            # TODO: Allow for explicit libraries to distinguish between debug and release
            bin_suffix = self._shared_lib_suffix()
            bin_suffix = '' if bin_suffix is None else bin_suffix
            imported_kwargs = {
                'lib_dir': self._lib_dir,
                'release_lib_file': f'{lib_name}{bin_suffix}',
                'debug_lib_file': f'{lib_name}{bin_suffix}',
            }
            # TODO: Allow for explicit libraries to distinguish between debug and release
            if self._implib_dir:
                imported_kwargs['implib_dir'] = self._implib_dir
                imported_kwargs['release_implib_file'] = f'{lib_name}.lib'
                imported_kwargs['debug_implib_file'] = f'{lib_name}.lib'

            lib_target.type_flags |= IMPORTED
            lib_target.imported(**imported_kwargs)
            self._unpack_artifacts.append(imported_kwargs)
            self._target.requires(lib_target_name, )
            self._shared_lib_targets.append(lib_target)

        # TODO: Handle static libraries

        app_names = self._auxiliary_apps
        for app_name in app_names:
            imported_kwargs = {
                'bin_dir': self._bin_dir,
                'bin_file': f'{app_name}',
            }
            self._unpack_artifacts.append(imported_kwargs)
        super().build()
        if self._include_dir:
            self._target.include_paths(self._include_dir, )
            for target in self._shared_lib_targets:
                target.include_paths(self._include_dir, )

        return self._shared_lib_targets + self._static_lib_targets

    @staticmethod
    def _shared_lib_suffix():
        if Env.platform.windows:
            return '.dll'
        elif Env.platform.macos:
            # TODO: macOS can output a .so too, probably need the compiler context here too to
            #  know for sure what kind it will output (e.g. AppleClang vs GCC)
            return '.dylib'
        elif Env.platform.linux:
            return '.so'
        return None

    @staticmethod
    def _app_suffix():
        if Env.platform.windows:
            return '.exe'
        return ''

    @staticmethod
    def app_suffix():
        bin_suffix = PrecompiledArchiveBuilder._app_suffix()
        return '' if bin_suffix is None else bin_suffix


# TODO: Get rid of Git builder and just make this simple kwargs, only the archive types will have builders given they
#  are a bit more involved, but they could also switch away from that if we wanted
class GitBuilder(Builder):
    def __init__(self, third_party_target):
        super().__init__(third_party_target)
        self._repository: Optional[str] = None
        self._tag: Optional[str] = None

    def repository(self, repository: str):
        self._repository = repository

    def tag(self, tag: str):
        self._tag = tag

    def build(self) -> None:
        self._target.properties['git_clone_dir'] = RootRelativeBinaryDir('_git')
        # TODO: include_paths is not just for the targets transitive includes, it is possible to have include paths
        #  outside of the target. We'll probably be fine here for now given this is for a third party target only,
        #  but this should still get cleaned up/improved
        include_paths = self._target.properties.get('include_paths', [])
        for include_dir in include_paths:
            include_dir.prepend('_git')
        source_files = self._target.properties.get('sources', {})
        for src_dir, src_files in source_files.items():
            src_dir.prepend('_git')

        self._target.properties['git_repository'] = self._repository
        self._target.properties['git_tag'] = self._tag
