"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
import subprocess
import tempfile
from typing import cast, Optional
from iprm.util.env import Env
from iprm.util.loader import Loader
from iprm.backend.backend import Backend
from iprm.api.project import Project, SubDir
from iprm.api.target import Target
from iprm.api.cpp import CppTarget
from iprm.api.rust import RustTarget


class Dot(Backend):
    def __init__(self, loader: Loader, **kwargs):
        super().__init__(loader, **kwargs)
        self._native_loader = cast(Loader, self.loader)

    @classmethod
    def png_icon_path(cls) -> Path:
        return Path(__file__).parent / 'dot.png'

    @classmethod
    def generate_file_exts(cls) -> list[str]:
        return ['dot']

    def _generate_file_name(self) -> str:
        return f'{self._native_loader.project_object.name}.{self.generate_file_exts()[0]}'

    def _generate_file_path(self) -> Path:
        return Path(self._native_loader.project_dir)

    def _generate_file_write_mode(self) -> str:
        return 'w' if self._is_root_item else 'a'

    def _generate_file_comment(self):
        return '//'

    def _add_generated_file_header(self) -> bool:
        return self._is_root_item

    def _add_generated_file_footer(self) -> bool:
        return self._is_last_item

    def _generate_file_footer(self) -> str:
        return '}'

    @classmethod
    def build(cls, **kwargs):
        if Env.platform.windows:
            cls._build_win(**kwargs)
        else:
            cls._build_unix(**kwargs)

    @classmethod
    def _build_win(cls, **kwargs):
        binary_dir = kwargs.get('bindir')
        temp_script_path: Optional[str] = None
        with tempfile.NamedTemporaryFile(suffix='.bat', delete=False, mode='w') as dot_svg_batch:
            temp_script_path = dot_svg_batch.name
            svg_file = f'{binary_dir}.svg'
            dot_svg_batch.write(f'''@echo off
dot -Tsvg {binary_dir} -o {svg_file}
start "" "{svg_file}"
''')
        subprocess.check_call([temp_script_path])

    @classmethod
    def _build_unix(cls, **kwargs):
        open_cmd = 'xdg-open' if Env.platform.linux else 'open'
        binary_dir = kwargs.get('bindir')
        temp_script_path: Optional[str] = None
        with tempfile.NamedTemporaryFile(suffix='.sh', delete=False, mode='w') as dot_svg_batch:
            temp_script_path = dot_svg_batch.name
            svg_file = f'{binary_dir}.svg'
            dot_svg_batch.write(f'''#!/bin/sh
dot -Tsvg {binary_dir} -o {svg_file}
{open_cmd} "{svg_file}"
''')
        import os, stat
        st = os.stat(temp_script_path)
        os.chmod(temp_script_path, st.st_mode | stat.S_IEXEC)
        subprocess.check_call([temp_script_path])

    def _generate_project(self, project: Project) -> list[str]:
        project_name = project.name
        return [
            f'digraph {project_name} {{',
            f'\tlabel=<<font point-size="24"><b>{project_name} [{self._native_loader.platform_display}]</b></font>>;',
            '\trankdir=RL;',
            '\tlabelloc=t;',
            '\tlabeljust=c;',
        ]

    def _generate_subdir(self, subdir: SubDir) -> list[str]:
        pass

    def _generate_target(self, target: Target) -> list[str]:
        target_name = target.name
        dot_content = [
            f'\t"{target_name}" [label="{target_name}", style=filled, shape={target.shape_type} fillcolor="{target.hex_colour}"];'
        ]
        for dependency in target.dependencies:
            dot_content.append(f'\t"{target_name}" -> "{dependency}";')
        return dot_content

    def _generate_cpp(self, cpp: CppTarget) -> list[str]:
        return self._generate_target(cpp)

    def _generate_rust(self, rust: RustTarget) -> list[str]:
        return self._generate_target(rust)
