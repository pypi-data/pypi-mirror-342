"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import uuid
from contextlib import contextmanager
from typing import Any, Optional
from iprm.core.core import Object as _Object
from iprm.core.typeflags import TypeFlags
from iprm.util.env import Env
from iprm.util.dir import RootRelativeSourceDir
from iprm.util.platform import PLATFORM_CTX_KEY, PlatformContext
from iprm.util.compiler import COMPILER_FLAGS_KEY

_object_created_callback: Optional[callable] = None


@contextmanager
def object_created_callback(on_object_created: callable):
    global _object_created_callback
    _object_created_callback = on_object_created
    try:
        yield
    finally:
        _object_created_callback = None


class Object(_Object):
    def __init__(self, name: str):
        super().__init__(name)
        from iprm.core.session import Session
        Session.register_object(self)
        # TODO: Working around the issues with trying to get the python layer to
        #  directly receive/work with the core c++ layer, as when I tried to switch
        #  to that method in order to avoid registering callbacks in the core, it then broke all
        #  type/inheritance information. Must be a way around this, but this is good
        #  enough for now and more or less what I had started with anyways, just not nested
        #  all the way down in the core, so we can live with it for now
        if _object_created_callback is not None:
            _object_created_callback(self)
        self.hex_colour = '#454545'
        self.shape_type = 'rectangle'
        self.root_relative_dir = RootRelativeSourceDir()
        self.properties: dict[str, Any] = {
            PLATFORM_CTX_KEY: {},
            COMPILER_FLAGS_KEY: {},
        }
        self._parent_path = Env.meta.build_file.parent
        self._uuid: str = str(uuid.uuid4()).upper() if Env.meta.msbuild else ''

    @property
    def parent_path(self):
        return self._parent_path

    @classmethod
    def svg_icon_path(cls):
        pass

    @property
    def uuid(self):
        return self._uuid

    # NOTE: The current shape types you see below are the only 4 supported right now for dependency graph rendering
    def rectangle(self):
        self.shape_type = 'rectangle'

    def circle(self):
        self.shape_type = 'circle'

    def diamond(self):
        self.shape_type = 'diamond'

    def ellipse(self):
        self.shape_type = 'ellipse'

    def platform_supports_property(self, platform_ctx: PlatformContext, prop: str):
        from iprm.util.platform import PLATFORM_CTX_KEY, platform_context, Platform
        prop_platform_contexts = self.properties[PLATFORM_CTX_KEY].get(prop, [])
        if not prop_platform_contexts:
            return False
        for prop_ctx in prop_platform_contexts:
            with platform_context(prop_ctx):
                if platform_ctx == Platform():
                    return True
        return False

    def compiler_supports_property(self, compiler_flag: TypeFlags, prop: str):
        from iprm.util.compiler import COMPILER_FLAGS_KEY
        prop_compiler_flags = self.properties[COMPILER_FLAGS_KEY].get(prop, TypeFlags.NONE)
        if prop_compiler_flags == TypeFlags.NONE:
            return False
        return compiler_flag & prop_compiler_flags
