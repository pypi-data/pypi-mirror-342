"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
from iprm.api.cpp import CppThirdParty
from iprm.util.dir import BinaryDir
from iprm.core.typeflags import PYTHON


# https://github.com/pybind/pybind11
class PyBind11ThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= PYTHON
        self.hex_colour = '#738AFF'
        self.header()
        self.include_paths(
            BinaryDir('include'),
        )

    @classmethod
    def svg_icon_path(cls):
        # https://www.python.org/community/logos
        return Path(__file__).parent / 'python.svg'
