"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from typing import Any, Optional
from iprm.core.object import Object
from iprm.core.typeflags import PROJECT, SUBDIR, TypeFlags
from iprm.util.env import Env
from iprm.util.platform import PlatformContext
from iprm.util.compiler import COMPILER_NAME_KEY, CPP_COMPILER_FLAGS, CPP_COMPILER_BINARIES, RUST_COMPILER_FLAGS, \
    RUST_COMPILER_BINARIES
from iprm.api.cpp import CppTarget
from iprm.api.rust import RustTarget


# TODO: Add ability to specify/limit the available platforms for this project, that way in Studio we only load and
#  prompt for the specified/supported platforms, instead of all of them
class Project(Object):
    def __init__(self, *args, **kwargs):
        version = kwargs.pop('version', None)
        description = kwargs.pop('description', None)
        url = kwargs.pop('url', None)
        platforms: Optional[list[PlatformContext]] = kwargs.pop('platforms', None)
        super().__init__(*args, **kwargs)
        if version:
            self.properties['version'] = version
        if description:
            self.properties['description'] = description
        if url:
            self.properties['url'] = url
        if platforms:
            self.properties['platforms'] = platforms
        self.type_flags = PROJECT
        self.hex_colour = '#FFC107'
        self.shape_type = 'star'
        self._root_dir = Env.meta.build_file.parent
        self._cpp_enabled = False
        self._cpp_compiler_name: str = CppTarget.default_compiler_name()
        self._cpp_compiler_flag: TypeFlags = CPP_COMPILER_FLAGS[CppTarget.default_compiler_name()]
        self._cpp_compiler_bin: str = CPP_COMPILER_BINARIES[CppTarget.default_compiler_name()]
        self._rust_enabled = False
        self._rust_compiler_name: str = RustTarget.default_compiler_name()
        self._rust_compiler_flag: TypeFlags = RUST_COMPILER_FLAGS[RustTarget.default_compiler_name()]
        self._rust_compiler_bin: str = RUST_COMPILER_BINARIES[RustTarget.default_compiler_name()]
        self.properties['options']: dict[str, dict[str, Any]] = {}

    @property
    def root_dir(self):
        return self._root_dir

    def option(self, option, default_value, description):
        self.properties['options'][option] = {
            'type': type(default_value),
            'default': default_value,
            'description': description,
        }

    # TODO: Support creating a option-based condition block within IPRM, need to enhance the loader/API to be able to
    #  do this, as we want the objects in the conditional to always be loaded, but still want to detect that said
    #  conditional was initiated.  Given the API is declarative, maybe we just invoke an method on that takes in the
    #  option name, a condition (if not specified assume option type is a bool), and then a lambda/callable for the
    #  condition satisfied and condition unsatisfied case

    def cpp(self, **kwargs):
        kwargs = CppTarget.default_language_properties(**kwargs)
        self._cpp_compiler_name = kwargs.get(COMPILER_NAME_KEY, CppTarget.default_compiler_name())
        self._cpp_compiler_flag = CPP_COMPILER_FLAGS[self._cpp_compiler_name]
        self._cpp_compiler_bin = CPP_COMPILER_BINARIES[self._cpp_compiler_name]
        self._enable_language(CppTarget.__name__, **kwargs)
        self._cpp_enabled = True

    @property
    def cpp_enabled(self):
        return self._cpp_enabled

    def cpp_compiler_flag(self) -> TypeFlags:
        return self._cpp_compiler_flag

    def cpp_compiler_binary(self):
        return self._cpp_compiler_bin

    def rust(self, **kwargs):
        kwargs = RustTarget.default_language_properties(**kwargs)
        self._rust_compiler_name = kwargs.get(COMPILER_NAME_KEY, RustTarget.default_compiler_name())
        self._rust_compiler_flag = RUST_COMPILER_FLAGS[self._rust_compiler_name]
        self._rust_compiler_bin = RUST_COMPILER_BINARIES[self._rust_compiler_name]
        self._enable_language(RustTarget.__name__, **kwargs)
        self._rust_enabled = True

    @property
    def rust_enabled(self):
        return self._rust_enabled

    def rust_compiler_flag(self) -> TypeFlags:
        return self._rust_compiler_flag

    def rust_compiler_binary(self):
        return self._rust_compiler_bin

    def _enable_language(self, language: str, **kwargs):
        if 'languages' not in self.properties:
            self.properties['languages'] = {}
        self.properties['languages'][language] = kwargs


class SubDir(Object):
    def __init__(self, name):
        self.path = Env.meta.build_file.parent / name
        super().__init__(name=str(self.path))
        self.type_flags = SUBDIR
        self.hex_colour = '#607D8B'
        self.shape_type = 'circle'
        self.properties['dir_name'] = name
        self.properties['dir_path'] = self.path
