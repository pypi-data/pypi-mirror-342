import os
import platform
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys

root_dir_path = os.path.dirname(__file__)
src_dir_path = os.path.abspath(os.path.join(root_dir_path, 'src'))
src_iprm_util_dir_path = os.path.join(src_dir_path, 'iprm', 'util')
sys.path.append(src_iprm_util_dir_path)


class CMakeExtension(Extension):
    def __init__(self, name):
        Extension.__init__(self, name, sources=[])


class IPRMBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(['ninja', '--version'])
        except OSError:
            raise RuntimeError("Ninja must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def _build(self, configure_cmd, build_cmd, cwd):
        from vcvarsall import vcvarsall_script
        if platform.system() == "Windows":
            subprocess.check_call(vcvarsall_script(' '.join(configure_cmd)), cwd=cwd)
            subprocess.check_call(vcvarsall_script(' '.join(build_cmd)), cwd=cwd)
        else:
            subprocess.check_call(configure_cmd, cwd=cwd)
            subprocess.check_call(build_cmd, cwd=cwd)

    def _build_core(self):
        configure = [
            'cmake',
            '-G', 'Ninja',
            '-S', '.',
            '-B', 'build_core',
            '-DCMAKE_BUILD_TYPE=RelWithDebInfo',
            '--fresh',
        ]
        build = [
            'cmake',
            '--build', 'build_core',
            '--config', 'RelWithDebInfo',
            '--parallel',
            '--verbose',
        ]
        src_iprm_core_dir_path = os.path.join(src_dir_path, 'iprm', 'core')
        self._build(configure, build, src_iprm_core_dir_path)

    def _build_studio(self):
        src_iprm_studio_dir_path = os.path.join(src_dir_path, 'iprm', 'studio')
        src_iprm_plugins_dir_path = os.path.join(src_dir_path, 'iprm', 'plugins')

        generate = [
            sys.executable,
            'iprm/cli/app.py',
            'generate',
            '--backend',
            'CMake',
            '--projdir',
            src_iprm_studio_dir_path,
            '--plugindir',
            src_iprm_plugins_dir_path,
        ]
        env = os.environ.copy()
        env['PYTHONPATH'] = os.pathsep.join([env.get('PYTHONPATH', ''), src_dir_path])
        subprocess.check_call(generate, cwd=src_dir_path, env=env)

        binary_dir_path = os.path.join(src_iprm_studio_dir_path, 'build_studio')

        configure = [
            sys.executable,
            'iprm/cli/app.py',
            'configure',
            '--backend',
            'CMake',
            '--ninja',
            '--srcdir',
            src_iprm_studio_dir_path,
            '--bindir',
            binary_dir_path,
            '--release',
        ]
        build = [
            sys.executable,
            'iprm/cli/app.py',
            'build',
            '--backend',
            'CMake',
            '--bindir',
            binary_dir_path,
            '--release',
        ]
        self._build(configure, build, src_dir_path)

    def build_extension(self, ext):
        if isinstance(ext, CMakeExtension):
            self._build_core()
            self._build_studio()


setup(
    ext_modules=[CMakeExtension("IPRM Core and Extension Modules"), ],
    cmdclass={"build_ext": IPRMBuild},
)
