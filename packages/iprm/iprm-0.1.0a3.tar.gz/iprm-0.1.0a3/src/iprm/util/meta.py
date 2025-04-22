from contextlib import contextmanager
from pathlib import Path
from typing import Optional

_current_backend: str = '<iprm_backend>'
_current_build_file: Optional[Path] = None


@contextmanager
def meta_context(backend: str, build_file: Path):
    global _current_backend
    previous_backend = _current_backend
    _current_backend = backend
    global _current_build_file
    previous_build_file = _current_build_file
    _current_build_file = build_file
    try:
        yield
    finally:
        _current_backend = previous_backend
        _current_build_file = previous_build_file


class Meta:
    def __init__(self, loading=False):
        global _current_backend
        self.backend = _current_backend
        if loading:
            from iprm.backend.cmake import CMake
            from iprm.backend.meson import Meson
            from iprm.backend.scons import SCons
            from iprm.backend.msbuild import MSBuild
            self.cmake = _current_backend == CMake.__name__
            self.meson = _current_backend == Meson.__name__
            self.scons = _current_backend == SCons.__name__
            self.msbuild = _current_backend == MSBuild.__name__
        else:
            self.cmake = False
            self.meson = False
            self.scons = False
            self.msbuild = False

        global _current_build_file
        self.build_file: Path = _current_build_file.resolve() if _current_build_file is not None else None
