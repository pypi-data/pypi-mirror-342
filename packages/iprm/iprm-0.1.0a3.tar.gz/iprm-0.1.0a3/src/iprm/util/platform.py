import platform as _platform
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from typing import Optional, Type
from iprm.core.session import Session


class ArchitectureContext:
    def __init__(self):
        self._x86_64 = False
        self._aarch64 = False
        self._riscv64 = False
        machine = _platform.machine().lower()
        if machine in ('x86_64', 'amd64', 'x64'):
            self._x86_64 = True
        elif machine in ('aarch64', 'arm64'):
            self._aarch64 = True
        elif machine in ('riscv64', 'riscv'):
            self._riscv64 = True
        else:
            raise ValueError(f'Architecture {machine} is not currently supported')

    @property
    def x86_64(self):
        return self._x86_64

    @property
    def aarch64(self):
        return self._aarch64

    @property
    def riscv64(self):
        return self._riscv64


WINDOWS_PLAT_NAME = 'Windows'
MACOS_PLAT_NAME = 'Darwin'
LINUX_PLAT_NAME = 'Linux'
WASM_PLAT_NAME = 'Web Assembly'

# TODO: Add support for iOS and Android
PLATFORMS = [WINDOWS_PLAT_NAME, MACOS_PLAT_NAME, LINUX_PLAT_NAME, WASM_PLAT_NAME]

PLAT_DISPLAY_NAME = {
    WINDOWS_PLAT_NAME: WINDOWS_PLAT_NAME,
    MACOS_PLAT_NAME: 'macOS',
    LINUX_PLAT_NAME: LINUX_PLAT_NAME,
    WASM_PLAT_NAME: WASM_PLAT_NAME,
}


@dataclass
class PlatformContext:
    windows: bool = False
    macos: bool = False
    linux: bool = False
    wasm: bool = False

    def __str__(self):
        if self.windows:
            return PLAT_DISPLAY_NAME[WINDOWS_PLAT_NAME]
        elif self.macos:
            return PLAT_DISPLAY_NAME[MACOS_PLAT_NAME]
        elif self.linux:
            return PLAT_DISPLAY_NAME[LINUX_PLAT_NAME]
        elif self.wasm:
            return PLAT_DISPLAY_NAME[WASM_PLAT_NAME]
        raise


@dataclass
class WindowsPlatformContext(PlatformContext):
    windows: bool = True


@dataclass
class MacOSPlatformContext(PlatformContext):
    macos: bool = True


class LinuxDistroContext:
    def __init__(self):
        self._info = self._get_distro_info()
        self._distro_id = self._info.get('id', 'unknown').lower()
        self._version = self._info.get('version', 'unknown')
        self._id_like = self._info.get('like', '').lower().split()

    @staticmethod
    def _get_distro_info():
        try:
            with open('/etc/os-release', 'r') as f:
                distro_info = {}
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        distro_info[key] = value.strip('"')
                return {
                    'name': distro_info.get('NAME', 'Unknown'),
                    'version': distro_info.get('VERSION_ID', 'Unknown'),
                    'id': distro_info.get('ID', 'Unknown'),
                    'like': distro_info.get('ID_LIKE', '')
                }
        except FileNotFoundError:
            return {'name': 'Unknown', 'version': 'Unknown', 'id': 'Unknown', 'like': ''}

    @property
    def version(self):
        return self._version

    @property
    def ubuntu(self):
        return self._distro_id == 'ubuntu'

    @property
    def debian(self):
        return self._distro_id == 'debian'

    @property
    def centos(self):
        return self._distro_id == 'centos'

    @property
    def fedora(self):
        return self._distro_id == 'fedora'

    @property
    def rhel(self):
        return self._distro_id == 'rhel'

    @property
    def arch(self):
        return self._distro_id == 'arch'

    @property
    def mint(self):
        return self._distro_id == 'linuxmint'

    @property
    def opensuse(self):
        return self._distro_id in ('opensuse', 'opensuse-leap', 'opensuse-tumbleweed')

    @property
    def void(self):
        return self._distro_id == 'void'

    @property
    def nixos(self):
        return self._distro_id == 'nixos'

    @property
    def debian_like(self):
        return 'debian' in self._id_like or self._distro_id == 'debian'

    @property
    def rhel_like(self):
        return 'rhel' in self._id_like or self._distro_id in ('rhel', 'centos', 'fedora')

    @property
    def arch_like(self):
        return 'arch' in self._id_like or self._distro_id == 'arch'


@dataclass
class LinuxPlatformContext(PlatformContext):
    linux: bool = True
    distro: LinuxDistroContext = LinuxDistroContext()


@dataclass
class WebAssemblyPlatformContext(PlatformContext):
    wasm: bool = True


PLAT_CONTEXT_TYPE = {
    WINDOWS_PLAT_NAME: WindowsPlatformContext,
    MACOS_PLAT_NAME: MacOSPlatformContext,
    LINUX_PLAT_NAME: LinuxPlatformContext,
    WASM_PLAT_NAME: WebAssemblyPlatformContext,
}

_current_platform_context: Optional[PlatformContext] = None


def is_platform_ctx_set():
    return _current_platform_context is not None


def active_platform_name():
    ctx = _current_platform_context
    if ctx is None:
        return _platform.system()
    if ctx.windows:
        return WINDOWS_PLAT_NAME
    elif ctx.macos:
        return MACOS_PLAT_NAME
    elif ctx.linux:
        return LINUX_PLAT_NAME
    elif ctx.wasm:
        return WASM_PLAT_NAME
    raise


@contextmanager
def platform_context(platform_ctx: PlatformContext):
    global _current_platform_context
    previous_context = _current_platform_context
    _current_platform_context = platform_ctx
    Session.begin_platform_context(active_platform_name())
    try:
        yield
    finally:
        Session.end_platform_context()
        _current_platform_context = previous_context


class Platform:
    arch = ArchitectureContext()

    def __init__(self):
        global _current_platform_context
        if _current_platform_context is not None:
            self.windows = _current_platform_context.windows
            self.macos = _current_platform_context.macos
            self.linux = _current_platform_context.linux
            self.wasm = _current_platform_context.wasm
        else:
            os_name = _platform.system()
            self.windows = os_name == WINDOWS_PLAT_NAME
            self.macos = os_name == MACOS_PLAT_NAME
            self.linux = os_name == LINUX_PLAT_NAME
            self.wasm = os_name == WASM_PLAT_NAME

    def __eq__(self, other):
        return (self.windows == other.windows and
                self.macos == other.macos and
                self.linux == other.linux and
                self.wasm == other.wasm)

    @staticmethod
    def display_name():
        return PLAT_DISPLAY_NAME[active_platform_name()]


PLATFORM_CTX_KEY = 'platform_ctx'


def platform(platform_context_class: Type[PlatformContext]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            from iprm.core.object import Object
            if isinstance(self, Object):
                if func.__name__ not in self.properties[PLATFORM_CTX_KEY]:
                    self.properties[PLATFORM_CTX_KEY][func.__name__] = []
                self.properties[PLATFORM_CTX_KEY][func.__name__].append(platform_context_class())
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


windows = platform(WindowsPlatformContext)
macos = platform(MacOSPlatformContext)
linux = platform(LinuxPlatformContext)
wasm = platform(WebAssemblyPlatformContext)
