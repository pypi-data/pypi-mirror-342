from iprm.util.platform import Platform, WindowsPlatformContext, MacOSPlatformContext, LinuxPlatformContext, \
    WebAssemblyPlatformContext
from iprm.util.meta import Meta


class Env:
    platform = Platform()
    windows = WindowsPlatformContext()
    macos = MacOSPlatformContext()
    linux = LinuxPlatformContext()
    wasm = WebAssemblyPlatformContext()
    meta = Meta()
