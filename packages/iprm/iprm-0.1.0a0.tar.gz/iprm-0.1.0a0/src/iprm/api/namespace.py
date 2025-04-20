"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.util.env import Env
from iprm.util.dir import CurrentSourceDir, SourceDir, RootRelativeSourceDir, CurrentBinaryDir, BinaryDir, \
    RootRelativeBinaryDir
from iprm.api.project import Project, SubDir
from iprm.api.cpp import (CppExecutable, CppStaticLibrary, CppSharedLibrary, CppTest, CppPythonModule,
                          CppThirdParty, QtThirdParty)
from iprm.api.builder import SourceArchiveBuilder, PrecompiledArchiveBuilder, GitBuilder
from iprm.api.rust import RustExecutable
from iprm.core.typeflags import NONE, PROJECT, SUBDIR, CPP, THIRDPARTY, QT, RUST, PYTHON

GENERAL_CATAGEORY_KEY = 'General'
GENERAL_CATEGORY = {
    GENERAL_CATAGEORY_KEY: [
        {Project.__name__: PROJECT},
        {SubDir.__name__: SUBDIR},
    ],
}

CPP_CATAGEORY_KEY = 'C++'
CPP_CATEGORY = {
    'C++': [
        {CppExecutable.__name__: CPP},
        {CppStaticLibrary.__name__: CPP},
        {CppSharedLibrary.__name__: CPP},
        {CppTest.__name__: CPP},
        {CppPythonModule.__name__: CPP | PYTHON},

        {CppThirdParty.__name__: THIRDPARTY | CPP},
        {QtThirdParty.__name__: THIRDPARTY | CPP | QT},
    ],
}

RUST_CATEGORY_KEY = 'Rust'
RUST_CATEGORY = {
    RUST_CATEGORY_KEY: [
        {RustExecutable.__name__: RUST},
    ],
}

OBJECT_CATEGORIES = {
    **GENERAL_CATEGORY,
    **CPP_CATEGORY,
    **RUST_CATEGORY,
}

UTILITY_CATEGORY = {
    'Utilities': [
        {Env.__name__: NONE},
        {CurrentSourceDir.__name__: NONE},
        {SourceDir.__name__: NONE},
        {RootRelativeSourceDir.__name__: NONE},
        {CurrentBinaryDir.__name__: NONE},
        {BinaryDir.__name__: NONE},
        {RootRelativeBinaryDir.__name__: NONE},
        {SourceArchiveBuilder.__name__: NONE},
        {PrecompiledArchiveBuilder.__name__: NONE},
        {GitBuilder.__name__: NONE},
    ],
}

NAMESPACE = {
    # Utilities
    Env.__name__: Env,
    CurrentSourceDir.__name__: CurrentSourceDir,
    SourceDir.__name__: SourceDir,
    RootRelativeSourceDir.__name__: RootRelativeSourceDir,
    CurrentBinaryDir.__name__: CurrentBinaryDir,
    BinaryDir.__name__: BinaryDir,
    RootRelativeBinaryDir.__name__: RootRelativeBinaryDir,
    SourceArchiveBuilder.__name__: SourceArchiveBuilder,
    PrecompiledArchiveBuilder.__name__: PrecompiledArchiveBuilder,
    GitBuilder.__name__: GitBuilder,

    # General
    Project.__name__: Project,
    SubDir.__name__: SubDir,

    # C++ Targets
    CppExecutable.__name__: CppExecutable,
    CppStaticLibrary.__name__: CppStaticLibrary,
    CppSharedLibrary.__name__: CppSharedLibrary,
    CppTest.__name__: CppTest,
    CppPythonModule.__name__: CppPythonModule,

    CppThirdParty.__name__: CppThirdParty,
    QtThirdParty.__name__: QtThirdParty,

    # Rust Targets
    RustExecutable.__name__: RustExecutable,
}
