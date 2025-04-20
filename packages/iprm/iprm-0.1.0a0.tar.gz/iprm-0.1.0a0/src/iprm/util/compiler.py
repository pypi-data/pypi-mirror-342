from functools import wraps
from iprm.core.typeflags import TypeFlags, MSVC, CLANG, GCC, EMSCRIPTEN, RUSTC

COMPILER_NAME_KEY = 'compiler'

STANDARD_VERSION_ARG = '--version'

# CPP
MSVC_COMPILER_NAME = 'msvc'
MSVC_CLANG_COMPILER_NAME = 'msvc-clang'
CLANG_COMPILER_NAME = 'clang'
GCC_COMPILER_NAME = 'gcc'
EMSCRIPTEN_COMPILER_NAME = 'emscripten'

CPP_COMPILER_FLAGS = {
    MSVC_COMPILER_NAME: MSVC,
    MSVC_CLANG_COMPILER_NAME: CLANG,
    CLANG_COMPILER_NAME: CLANG,
    GCC_COMPILER_NAME: GCC,
    EMSCRIPTEN_COMPILER_NAME: EMSCRIPTEN,
}

CPP_COMPILER_BINARIES = {
    MSVC_COMPILER_NAME: 'cl',
    MSVC_CLANG_COMPILER_NAME: 'clang-cl',
    CLANG_COMPILER_NAME: 'clang++',
    GCC_COMPILER_NAME: 'g++',
    EMSCRIPTEN_COMPILER_NAME: 'em++',
}

# RUST
RUSTC_COMPILER_NAME = 'rustc'

RUST_COMPILER_FLAGS = {
    RUSTC_COMPILER_NAME: RUSTC,
}

RUST_COMPILER_BINARIES = {
    RUSTC_COMPILER_NAME: 'rustc'
}

COMPILER_FLAGS_KEY = 'compiler_flags'


def compiler(compiler_flag: TypeFlags):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            from iprm.core.object import Object
            if isinstance(self, Object):
                if func.__name__ not in self.properties[COMPILER_FLAGS_KEY]:
                    self.properties[COMPILER_FLAGS_KEY][func.__name__] = TypeFlags.NONE
                if self._compiler_flag == compiler_flag:
                    self.properties[COMPILER_FLAGS_KEY][func.__name__] |= compiler_flag
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


msvc = compiler(MSVC)
clang = compiler(CLANG)
gcc = compiler(GCC)
emscripten = compiler(EMSCRIPTEN)
rustc = compiler(RUSTC)
