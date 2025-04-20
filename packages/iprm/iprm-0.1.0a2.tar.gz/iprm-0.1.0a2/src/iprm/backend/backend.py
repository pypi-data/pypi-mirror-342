"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import os
import sys
import subprocess
from abc import ABC, abstractmethod
from enum import IntEnum
from pathlib import Path
from typing import Optional, Callable
from iprm.util.loader import Loader
from iprm.util.env import Env
from iprm.util.dir import Dir
from iprm.util.platform import PlatformContext
from iprm.util.vcvarsall import vcvarsall_script
from iprm.core.object import Object
from iprm.api.project import Project, SubDir
from iprm.api.target import Target
from iprm.api.cpp import CppTarget
from iprm.api.rust import RustTarget

iprm_gen_dir_path = os.path.dirname(__file__)
src_dir_path = os.path.abspath(os.path.join(iprm_gen_dir_path, '..', '..'))
sys.path.append(src_dir_path)


class GenerateMode(IntEnum):
    PER_FILE = 1
    PER_OBJECT = 2


class Backend(ABC):
    def __init__(self, loader: Loader, **kwargs):
        self._loader = loader
        # TODO: Use this for something
        self._config = kwargs
        self._is_root_item: Optional[bool] = None
        self._is_last_item: Optional[bool] = None
        self._current_generate_dir: Optional[Path] = None
        self._current_generated_file_header: Optional[str] = None

    @property
    def loader(self):
        return self._loader

    @property
    def project_dir_str(self):
        return str(self.loader.project_dir)

    def generate_project(self):
        project_objects = self.loader.load_project()
        nothing_to_generate_msg = 'no files to generate' if self._generate_mode() == GenerateMode.PER_FILE else 'no objects to generate'

        if project_objects is None:
            self.loader.log_sink.log_message(
                f"'{str(self.loader.platform_ctx)}' platform is not supported: {nothing_to_generate_msg}\n", error=True)
            return

        from itertools import chain
        num_items_to_generate = len(project_objects.keys()) if self._generate_mode() == GenerateMode.PER_FILE else len(
            list(chain.from_iterable(project_objects.values()))) if project_objects is not None else 0
        if num_items_to_generate == 0:
            self.loader.log_sink.log_message(nothing_to_generate_msg)
            return

        num_items_generated = 1
        for native_file_path, objects in project_objects.items():
            def gen_log(item):
                self.loader.log_sink.log_message(
                    f"[{num_items_generated}/{num_items_to_generate}] Generating '{item}' from "
                    f"'{native_file_path}'", end='\r')

            if self._generate_mode() == GenerateMode.PER_FILE:
                self._is_root_item = any([isinstance(obj, Project) for obj in objects])
            self._is_last_item = num_items_generated == num_items_to_generate
            self._current_generated_file_header = '\n'.join(self._generate_file_header())

            generate_file_name = self._generate_file_name()
            if self._generate_mode() == GenerateMode.PER_FILE:
                gen_log(generate_file_name)

            self._current_generate_dir = Path(str(native_file_path)).parent
            generated_content = []
            if self._generate_mode() == GenerateMode.PER_FILE and self._add_generated_file_header():
                generated_content.append(self._current_generated_file_header)

            for obj in objects:
                generate_object_name = obj.name

                if self._generate_mode() == GenerateMode.PER_OBJECT:
                    self._is_root_item = isinstance(obj, Project)
                    if isinstance(obj, SubDir):
                        # TODO: Currently only MSBuild uses PER_OBJECT generate mode, and it doesn't create explicit
                        #  files for a SubDir object, so for now we're just hardcoding to skip actual processing of
                        #  SubDirs
                        num_items_generated += 1
                        continue

                    generate_object_name = f'{obj.name}{self._generate_file_name()}'
                    gen_log(generate_object_name)
                generated_obj_content = self._generate_object(obj)
                if not generated_obj_content:
                    continue
                if self._generate_mode() == GenerateMode.PER_FILE:
                    generated_content.extend(generated_obj_content)
                elif self._generate_mode() == GenerateMode.PER_OBJECT:
                    generated_content = []
                    if self._add_generated_file_header():
                        generated_content.append(self._current_generated_file_header)
                    generated_content.extend(generated_obj_content)
                    if self._add_generated_file_footer():
                        generated_content.append(self._generate_file_footer())
                    generated_file_path = self._generate_file_path() / generate_object_name
                    if self._generate_file_write_impl(generated_file_path, generated_content):
                        num_items_generated += 1

            if self._generate_mode() == GenerateMode.PER_FILE:
                if self._add_generated_file_footer():
                    generated_content.append(self._generate_file_footer())
                generated_content.append('')
                generated_file_path = self._generate_file_path() / generate_file_name
                if self._generate_file_write_impl(generated_file_path, generated_content):
                    num_items_generated += 1

        self.loader.log_sink.log_message('')

    @classmethod
    def _generate_mode(cls):
        return GenerateMode.PER_FILE

    def _generate_file_path(self) -> Path:
        return self._current_generate_dir

    @abstractmethod
    def _generate_file_name(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def generate_file_exts(cls) -> list[str]:
        pass

    def _generate_file_write_mode(self) -> str:
        return 'w'

    def _generate_file_write_impl(self, generated_file_path, generated_content) -> bool:
        with open(generated_file_path, self._generate_file_write_mode()) as file:
            file.write('\n'.join(generated_content))
            return True
        return False

    def _generate_file_comment(self):
        return '#'

    def _generate_file_comment_prefix(self):
        pass

    def _generate_file_comment_suffix(self):
        pass

    def _add_generated_file_header(self) -> bool:
        return True

    def _generate_file_header(self):
        from iprm import __version__
        from datetime import datetime, timezone
        comment = self._generate_file_comment()
        comment_prefix = f'{self._generate_file_comment_prefix() if comment is None else comment} '
        comment_suffix = f' {self._generate_file_comment_suffix()}' if comment is None else ''
        return [
            f'{comment_prefix}========================================================={comment_suffix}',
            f'{comment_prefix}WARNING: This file is auto-generated. DO NOT EDIT MANUALLY{comment_suffix}',
            f'{comment_prefix}Generated by: iprm (v{__version__}){comment_suffix}',
            f'{comment_prefix}Generated on: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")}{comment_suffix}',
            f'{comment_prefix}Platform: {self.loader.platform}{comment_suffix}',
            f'{comment_prefix}========================================================={comment_suffix}',
        ]

    def _add_generated_file_footer(self) -> bool:
        return False

    def _generate_file_footer(self) -> str:
        pass

    def _generate_object(self, obj: Object) -> list[str]:
        from typing import cast
        if obj.is_project:
            project = cast(Project, obj)
            return self._generate_project(project)
        elif obj.is_subdir:
            subdirs = cast(SubDir, obj)
            return self._generate_subdir(subdirs)
        elif obj.is_cpp:
            cpp = cast(CppTarget, obj)
            return self._generate_cpp(cpp)
        elif obj.is_rust:
            rust = cast(RustTarget, obj)
            return self._generate_rust(rust)
        return []

    @abstractmethod
    def _generate_project(self, project: Project) -> list[str]:
        pass

    @abstractmethod
    def _generate_subdir(self, subdir: SubDir) -> list[str]:
        pass

    @abstractmethod
    def _generate_target(self, target: Target) -> list[str]:
        pass

    @abstractmethod
    def _generate_cpp(self, cpp: CppTarget) -> list[str]:
        pass

    @classmethod
    def _cpp_header_file_exts(cls):
        return ['hpp', 'hh', 'hxx', 'h']

    @classmethod
    def _cpp_source_file_exts(cls):
        return ['cpp', 'cc', 'cpp', 'c']

    @abstractmethod
    def _generate_rust(self, rust: RustTarget) -> list[str]:
        pass

    @classmethod
    def platforms(cls) -> list[PlatformContext]:
        return [Env.windows, Env.macos, Env.linux, Env.wasm]

    @classmethod
    def icon(cls) -> Path:
        pass

    @classmethod
    def dir_separator(cls):
        return '/'

    @classmethod
    def _run_command(cls, cmd, platform_ctx: PlatformContext = None):
        def cmd_wrapper(cmd_list):
            cmd_str = ' '.join(cmd_list)
            if not platform_ctx:
                return cmd_str
            # TODO: Once non-default platform compiler support is added, we should only use the vcvarsall script
            #  wrapper for MSVC (cl)/MSVC-Clang (clang-cl) compilers, as Windows can still use Mingw64 fcc/clang or
            #  clang via-MSVC target without needing to be in the Visual Studio dev environment
            if platform_ctx.windows:
                return vcvarsall_script(cmd_str)
            return cmd_str

        return subprocess.run(
            cmd_wrapper(cmd), shell=True).returncode

    @classmethod
    def configure(cls, **kwargs):
        pass

    # TODO: Add a `clean` command that cleans all generated files in the specified project dir (generated src and
    #  configured build/binary files). then update our cli test to do a clean command as the last step, so we can
    #  remove the testsuite-wide cleanup infra required and keep each test self contained

    @classmethod
    def build(cls, **kwargs):
        pass

    @classmethod
    def test(cls, **kwargs):
        pass

    @classmethod
    def install(cls, **kwargs):
        pass

    @classmethod
    def num_procs(cls, **kwargs):
        numproc = kwargs.get('numproc', None)
        if numproc:
            return numproc
        if Env.platform.windows:
            return '%NUMBER_OF_PROCESSORS%'
        elif Env.platform.macos:
            return '$(sysctl -n hw.ncpu)'
        elif Env.platform.linux:
            return '$(nproc)'
        return None

    @classmethod
    def build_type(cls, **kwargs):
        release = kwargs.get('release', None)
        bld_type = cls._default_build_type() if release is None else cls._release_build_type()
        debug = kwargs.get('debug', None)
        if debug:
            bld_type = cls._debug_build_type()
        return bld_type

    @classmethod
    def _default_build_type(cls):
        pass

    @classmethod
    def _release_build_type(cls):
        pass

    @classmethod
    def _debug_build_type(cls):
        pass


class BuildSystem(Backend):
    def __init__(self, loader: Loader, **kwargs):
        super().__init__(loader, **kwargs)

    @classmethod
    @abstractmethod
    def relative_src_path(cls, root_relative_path: Path, dir_path: Dir, leaf_path: str = None):
        pass

    @classmethod
    def relative_bin_path(cls, root_relative_path: Path, dir_path: Dir, leaf_path: str = None):
        pass

    @classmethod
    @abstractmethod
    def current_bin_dir(cls):
        pass

    @classmethod
    def _cpp_get_sources(cls, cpp: CppTarget, key: str, file_exts: list[str], exclude_mode: bool = False):
        source_file_paths = []
        root_relative_path = cpp.root_relative_dir.path
        sources_dict = cpp.properties.get(key, {})
        if sources_dict:
            for src_dir, src_files in sources_dict.items():
                for src_file in src_files:
                    matches_extension = any([Path(src_file).suffix == f'.{ext}' for ext in file_exts])
                    if (exclude_mode and not matches_extension) or (not exclude_mode and matches_extension):
                        relative_path_func = cls.relative_src_path
                        if src_dir.binary:
                            relative_path_func = cls.relative_bin_path
                        source_file_paths.append(relative_path_func(root_relative_path, src_dir, src_file))
        return source_file_paths

    @classmethod
    def _cpp_get_header_files(cls, cpp: CppTarget):
        return cls._cpp_get_sources(cpp, 'headers', cls._cpp_header_file_exts())

    @classmethod
    def _cpp_get_source_files(cls, cpp: CppTarget):
        return cls._cpp_get_sources(cpp, 'sources', cls._cpp_source_file_exts())

    @classmethod
    def _cpp_get_resource_files(cls, cpp: CppTarget):
        return cls._cpp_get_sources(cpp, 'sources', cls._cpp_source_file_exts(), exclude_mode=True)

    @classmethod
    def _cpp_get_header_src_file_paths(cls, cpp: CppTarget):
        return cls._cpp_get_header_files(cpp)

    @classmethod
    def _cpp_get_source_src_file_paths(cls, cpp: CppTarget):
        return cls._cpp_get_source_files(cpp)

    @classmethod
    def _cpp_get_resource_src_file_paths(cls, cpp: CppTarget):
        return cls._cpp_get_resource_files(cpp)


class ProjectModel(Backend):
    @classmethod
    @abstractmethod
    def generator_ninja(cls):
        pass

    @classmethod
    @abstractmethod
    def generator_xcode(cls):
        pass

    @classmethod
    @abstractmethod
    def generator_visual_studio(cls):
        pass

    @classmethod
    @abstractmethod
    def generator_unix_makefile(cls):
        pass

    @classmethod
    @abstractmethod
    def supports_posix_paths(cls):
        pass

    @classmethod
    @abstractmethod
    def src_dir(cls):
        pass

    @classmethod
    @abstractmethod
    def current_src_dir(cls):
        pass

    @classmethod
    @abstractmethod
    def relative_src_path(cls, dir_path: Dir, leaf_path: str = None):
        pass

    @classmethod
    @abstractmethod
    def bin_dir(cls):
        pass

    @classmethod
    @abstractmethod
    def current_bin_dir(cls):
        pass

    @classmethod
    @abstractmethod
    def relative_bin_path(cls, dir_path: Dir, leaf_path: str = None):
        pass

    @classmethod
    def _cpp_get_sources(cls, cpp: CppTarget, key: str, file_exts: list[str], relative_path_func: Callable):
        source_file_paths = []
        sources_dict = cpp.properties.get(key, {})
        if sources_dict:
            for src_dir, src_files in sources_dict.items():
                for src_file in src_files:
                    if any([Path(src_file).suffix == f'.{ext}' for ext in file_exts]):
                        source_file_paths.append(relative_path_func(src_dir, src_file))
        return source_file_paths

    @classmethod
    def _cpp_get_header_files(cls, cpp: CppTarget, relative_path_func: Callable):
        return cls._cpp_get_sources(cpp, 'headers', cls._cpp_header_file_exts(), relative_path_func)

    @classmethod
    def _cpp_get_source_files(cls, cpp: CppTarget, relative_path_func: Callable):
        return cls._cpp_get_sources(cpp, 'sources', cls._cpp_source_file_exts(), relative_path_func)

    @classmethod
    def _cpp_get_header_src_file_paths(cls, cpp: CppTarget):
        return cls._cpp_get_header_files(cpp, cls.relative_src_path)

    @classmethod
    def _cpp_get_source_src_file_paths(cls, cpp: CppTarget):
        return cls._cpp_get_source_files(cpp, cls.relative_src_path)

    @classmethod
    def _cpp_get_header_bin_file_paths(cls, cpp: CppTarget):
        return cls._cpp_get_header_files(cpp, cls.relative_bin_path)

    @classmethod
    def _cpp_get_source_bin_file_paths(cls, cpp: CppTarget):
        return cls._cpp_get_source_files(cpp, cls.relative_bin_path)

    @classmethod
    def _extract_precompiled_bin_artifact(cls, artifact):
        # TODO: Allow bin files to specify release/debug too
        return artifact.get('bin_file')

    @classmethod
    def _extract_precompiled_lib_artifact(cls, artifact):
        lib_release = artifact.get('release_lib_file')
        lib_debug = artifact.get('debug_lib_file', None)
        return lib_release, lib_debug

    @classmethod
    def _extract_precompiled_implib_artifact(cls, artifact):
        implib_release = artifact.get('release_implib_file')
        implib_debug = artifact.get('debug_implib_file', None)
        return implib_release, implib_debug

    @classmethod
    def _extract_precompiled_artifact(cls, artifact, key1, key2):
        return artifact.get(key1, artifact.get(key2, None))
