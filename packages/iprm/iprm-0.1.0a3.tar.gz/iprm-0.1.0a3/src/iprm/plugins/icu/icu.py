"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
from iprm.api.cpp import CppThirdParty


class IcuThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex_colour = '#5555FF'

    @classmethod
    def svg_icon_path(cls):
        # https://upload.wikimedia.org/wikipedia/commons/0/09/New_Unicode_logo.svg
        return Path(__file__).parent / 'unicode.svg'
