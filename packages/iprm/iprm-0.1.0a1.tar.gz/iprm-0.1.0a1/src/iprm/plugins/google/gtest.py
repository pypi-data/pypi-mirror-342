"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
from iprm.api.cpp import CppThirdParty
from iprm.util.dir import BinaryDir


# https://github.com/google/googletest
class GTestThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex_colour = '#4285F4'
        self.static()
        self.include_paths(
            BinaryDir('googletest'),
            BinaryDir('googletest', 'include'),
            BinaryDir('googlemock'),
            BinaryDir('googlemock', 'include'),
        )
        self.sources(
            BinaryDir('googletest', 'src'),
            'gtest-all.cc',
        )
        self.sources(
            BinaryDir('googlemock', 'src'),
            'gmock-all.cc',
        )

    @classmethod
    def svg_icon_path(cls):
        # https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg
        return Path(__file__).parent / 'google.svg'
