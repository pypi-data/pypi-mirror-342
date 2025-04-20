"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
from iprm.api.cpp import CppThirdParty


class BoostThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex_colour = '#FF9F00'

    @classmethod
    def svg_icon_path(cls):
        # https://github.com/boostorg/website-v2-docs/blob/develop/antora-ui/src/img/boost-logo-transparent.svg
        return Path(__file__).parent / 'boost.svg'
