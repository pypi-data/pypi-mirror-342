"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import argparse
import os
import sys
import platform


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from iprm.util.loader import Loader
from iprm.backend.cmake import CMake
from iprm.backend.meson import Meson
from iprm.backend.scons import SCons
from iprm.backend.msbuild import MSBuild
from iprm.core.session import Session
from iprm.util.platform import WASM_PLAT_NAME, PLAT_CONTEXT_TYPE
from iprm.util.plugins import load_backends

PROJECT_MODEL_BACKENDS = {
    CMake.__name__: CMake,
    Meson.__name__: Meson,
}

BUILD_SYSTEM_BACKENDS = {
    SCons.__name__: SCons,
    MSBuild.__name__: MSBuild,
}

supported_backends = PROJECT_MODEL_BACKENDS | BUILD_SYSTEM_BACKENDS

GENERATE_CMD = 'generate'
CONFIGURE_CMD = 'configure'
BUILD_CMD = 'build'
TEST_CMD = 'test'
INSTALL_CMD = 'install'


def _native_loader_main(command, **kwargs):
    project_dir = kwargs.pop('projdir')
    Session.create(project_dir)
    wasm = kwargs.pop('wasm')
    plugin_dir = kwargs.pop('plugin_dir')
    platform_name = WASM_PLAT_NAME if wasm else platform.system()
    loader = Loader(project_dir, platform_name, plugin_dir)
    if command == GENERATE_CMD:
        generator_class = supported_backends[kwargs.pop('backend')]
        loader.backend = generator_class.__name__
        generator = generator_class(loader, **kwargs)
        generator.generate_project()
    Session.destroy()


def _configure_main(**kwargs):
    backend = kwargs.pop('backend')
    wasm = kwargs.pop('wasm')
    platform_name = WASM_PLAT_NAME if wasm else platform.system()
    kwargs['platform_ctx'] = PLAT_CONTEXT_TYPE[platform_name]()
    generator_class = supported_backends[backend]
    if backend in PROJECT_MODEL_BACKENDS:
        if kwargs.pop('ninja', None):
            kwargs['generator'] = generator_class.generator_ninja()
        if kwargs.pop('xcode', None):
            kwargs['generator'] = generator_class.generator_xcode()
        if kwargs.pop('visual_studio', None):
            kwargs['generator'] = generator_class.generator_visual_studio()
        if kwargs.pop('unix_makefile', None):
            kwargs['generator'] = generator_class.generator_unix_makefile()
    sys.exit(generator_class.configure(**kwargs))


def _build_main(**kwargs):
    generator_class = supported_backends[kwargs.pop('backend')]
    wasm = kwargs.pop('wasm')
    platform_name = WASM_PLAT_NAME if wasm else platform.system()
    kwargs['platform_ctx'] = PLAT_CONTEXT_TYPE[platform_name]()
    sys.exit(generator_class.build(**kwargs))


def _test_main(**kwargs):
    generator_class = supported_backends[kwargs.pop('backend')]
    sys.exit(generator_class.test(**kwargs))


def _install_main(**kwargs):
    generator_class = supported_backends[kwargs.pop('backend')]
    sys.exit(generator_class.install(**kwargs))


def _validate_backend(value):
    if value not in supported_backends:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not supported. Use one of: {', '.join(supported_backends)}"
        )
    return value


def main(known_backend=None):
    parser = argparse.ArgumentParser(description='IPRM Command Line Interface')
    subparsers = parser.add_subparsers(
        dest='command',
        help='Command to execute'
    )

    plugin_parser = argparse.ArgumentParser(add_help=False)
    plugin_parser.add_argument(
        '--plugindir',
        help='Path to plugin modules that implement the Backend API'
    )

    loader_parser = argparse.ArgumentParser(add_help=False)
    loader_parser.add_argument(
        '-p', '--projdir',
        help='Root directory of the IPRM project'
    )

    backend_parser = argparse.ArgumentParser(add_help=False)
    backend_parser.add_argument(
        '--backend',
        required=False,
        help=argparse.SUPPRESS if not known_backend else 'Backend to use'
    )

    environment_parser = argparse.ArgumentParser(add_help=False)
    environment_parser.add_argument(
        '--wasm',
        action='store_true',
        default=False,
        help='Target web assembly platform via the Emscripten SDK'
    )

    backend_help_text = "the specified backend" if not known_backend else known_backend

    # TODO: Add some configuration here, e.g. enable/disable generation cache, by default it will be enabled
    _generate_parser = subparsers.add_parser('generate', help=f'Generate project files for {backend_help_text}',
                                             parents=[plugin_parser, backend_parser, loader_parser, environment_parser])

    execution_parser = argparse.ArgumentParser(add_help=False)
    execution_parser.add_argument(
        '--bindir',
        help='Root binary directory for the project'
    )
    # TODO: Add the equivalent of the 2 other types CMake natively supports, RelWithDebInfo and MinSizeRel
    build_type_parser = execution_parser.add_mutually_exclusive_group(required=False)
    build_type_parser.add_argument(
        '--release',
        action='store_true',
        help='Build with release configuration for the project'
    )
    build_type_parser.add_argument(
        '--debug',
        action='store_true',
        help='Build with debug configuration for the project'
    )

    configure_parser = subparsers.add_parser('configure',
                                             help=f'Configure the generated project files for {backend_help_text}',
                                             parents=[plugin_parser, backend_parser, execution_parser,
                                                      environment_parser])

    custom_generator_parser = configure_parser.add_mutually_exclusive_group(required=False)
    custom_generator_parser.add_argument(
        '--generator',
        help='Build System to generate project files for'
    )
    builtin_generator_parsers = configure_parser.add_mutually_exclusive_group(required=False)
    builtin_generator_parser = builtin_generator_parsers.add_mutually_exclusive_group()
    builtin_generator_parser.add_argument(
        '--ninja',
        action='store_true',
        help='Generate Ninja build files',
    )
    builtin_generator_parser.add_argument(
        '--xcode',
        action='store_true',
        help='Generate Xcode project',
    )
    builtin_generator_parser.add_argument(
        '--visual-studio',
        action='store_true',
        help='Generate Visual Studio project',
    )
    builtin_generator_parser.add_argument(
        '--unix-makefile',
        action='store_true',
        help='Generate Unix Makefiles',
    )

    configure_parser.add_argument(
        '--srcdir',
        required=True,
        help='Root source directory for the project'
    )

    # TODO: Expose arbitrary options specification here that overrides the default values set on the project
    #   Should not something like `-opt-<name>=<value>`

    build_parser = subparsers.add_parser('build',
                                         help=f'Build the generated project files for {backend_help_text}',
                                         parents=[plugin_parser, backend_parser, execution_parser, environment_parser])
    build_parser.add_argument(
        '--target',
        required=False,
        help='Target to build'
    )
    build_parser.add_argument(
        '--numproc',
        required=False,
        help='Number of available processors on your system to use in build'
    )
    build_parser.add_argument(
        '--solution',
        required=False,
        help='The name of the solution, identical to the project name (MSBuild Only)'
    )

    # TODO: Add some configuration here
    _test_parser = subparsers.add_parser('test',
                                         help=f'Test the generated project for {backend_help_text}',
                                         parents=[plugin_parser, backend_parser, execution_parser])

    # TODO: implement install command

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    kwargs = vars(args)
    command = kwargs.pop('command')
    backend: str = kwargs.pop('backend', '')
    if not backend:
        print(f'{command} requires a backend')
        return

    plugin_dir = kwargs.pop('plugindir', '')
    external_plugin_backends = load_backends(plugin_dir) if plugin_dir else {}
    supported_backends.update(**external_plugin_backends)

    internal_plugin_backends = load_backends(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plugins')))
    supported_backends.update(**internal_plugin_backends)

    backend = _validate_backend(backend)

    if command == GENERATE_CMD:
        _native_loader_main(command=command, backend=backend, plugin_dir=plugin_dir, **kwargs)
    elif command == CONFIGURE_CMD:
        _configure_main(backend=backend, **kwargs)
    elif command == BUILD_CMD:
        _build_main(backend=backend, **kwargs)
    elif command == TEST_CMD:
        _test_main(backend=backend, **kwargs)
    elif command == INSTALL_CMD:
        _install_main(backend=backend, **kwargs)


def _backend_main(backend):
    if len(sys.argv) >= 3:
        command = sys.argv[1]
        args = sys.argv[2:]
        backend_argv = [
            sys.argv[0],
            command,
            '--backend',
            backend,
        ]
        backend_argv.extend(args)
        sys.argv = backend_argv
        main(backend)


def cmake_main():
    _backend_main(CMake.__name__)


def meson_main():
    _backend_main(Meson.__name__)


def scons_main():
    _backend_main(SCons.__name__)


def msbuild_main():
    _backend_main(MSBuild.__name__)


if __name__ == '__main__':
    main()
