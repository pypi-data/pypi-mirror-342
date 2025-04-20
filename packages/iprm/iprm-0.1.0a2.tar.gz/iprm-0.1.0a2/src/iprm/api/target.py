"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.core.object import Object
from iprm.core.typeflags import TARGET
from iprm.util.dir import Dir


class Target(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags = TARGET
        self.properties['dependencies']: list[str] = []

    def requires(self, *targets: tuple[str]):
        self.properties['dependencies'].extend(targets)

    @property
    def dependencies(self):
        return self.properties.get('dependencies', [])

    def suffix(self, suffix: str):
        self.properties['suffix'] = suffix

    def server_port(self, port: int):
        self.properties['server_port'] = port
