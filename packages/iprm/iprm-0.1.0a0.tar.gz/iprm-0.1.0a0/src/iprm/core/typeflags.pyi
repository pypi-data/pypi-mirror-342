"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from enum import IntFlag
from typing import ClassVar


class TypeFlags(IntFlag):
    NONE: ClassVar[TypeFlags]
    PROJECT: ClassVar[TypeFlags]
    SUBDIR: ClassVar[TypeFlags]
    TARGET: ClassVar[TypeFlags]
    TEST: ClassVar[TypeFlags]
    EXECUTABLE: ClassVar[TypeFlags]
    LIBRARY: ClassVar[TypeFlags]
    HEADER: ClassVar[TypeFlags]
    STATIC: ClassVar[TypeFlags]
    SHARED: ClassVar[TypeFlags]
    GUI: ClassVar[TypeFlags]
    THIRDPARTY: ClassVar[TypeFlags]
    IMPORTED: ClassVar[TypeFlags]
    PKGCONFIG: ClassVar[TypeFlags]
    ARCHIVE: ClassVar[TypeFlags]
    PRECOMPILED: ClassVar[TypeFlags]
    SOURCE: ClassVar[TypeFlags]
    GIT: ClassVar[TypeFlags]
    VCPKG: ClassVar[TypeFlags]
    CONAN: ClassVar[TypeFlags]
    HOMEBREW: ClassVar[TypeFlags]
    SYSTEM: ClassVar[TypeFlags]
    DPKG: ClassVar[TypeFlags]
    RPM: ClassVar[TypeFlags]
    CONTAINER: ClassVar[TypeFlags]
    CRTSTATIC: ClassVar[TypeFlags]
    CRTDYNAMIC: ClassVar[TypeFlags]
    CRTDUAL: ClassVar[TypeFlags]
    CPP: ClassVar[TypeFlags]
    RUST: ClassVar[TypeFlags]
    PYTHON: ClassVar[TypeFlags]
    QT: ClassVar[TypeFlags]
    PYBIND11: ClassVar[TypeFlags]
    MSVC: ClassVar[TypeFlags]
    CLANG: ClassVar[TypeFlags]
    GCC: ClassVar[TypeFlags]
    EMSCRIPTEN: ClassVar[TypeFlags]
    RUSTC: ClassVar[TypeFlags]

    def __or__(self, other: TypeFlags) -> TypeFlags: ...

    def __and__(self, other: TypeFlags) -> TypeFlags: ...

    def __invert__(self) -> TypeFlags: ...

    def __int__(self) -> int: ...


# Export all enum values at module level
NONE: TypeFlags
PROJECT: TypeFlags
SUBDIR: TypeFlags
TARGET: TypeFlags
TEST: TypeFlags
EXECUTABLE: TypeFlags
LIBRARY: TypeFlags
HEADER: TypeFlags
STATIC: TypeFlags
SHARED: TypeFlags
GUI: TypeFlags
THIRDPARTY: TypeFlags
IMPORTED: TypeFlags
PKGCONFIG: TypeFlags
ARCHIVE: TypeFlags
PRECOMPILED: TypeFlags
SOURCE: TypeFlags
GIT: TypeFlags
VCPKG: TypeFlags
CONAN: TypeFlags
HOMEBREW: TypeFlags
SYSTEM: TypeFlags
DPKG: TypeFlags
RPM: TypeFlags
CONTAINER: TypeFlags
CRTSTATIC: TypeFlags
CRTDYNAMIC: TypeFlags
CRTDUAL: TypeFlags
CPP: TypeFlags
RUST: TypeFlags
PYTHON: TypeFlags
QT: TypeFlags
PYBIND11: TypeFlags
MSVC: TypeFlags
CLANG: TypeFlags
GCC: TypeFlags
EMSCRIPTEN: TypeFlags
RUSTC: TypeFlags
