"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
from iprm.util.loader import Loader
from iprm.backend.backend import BuildSystem
from iprm.util.dir import Dir, CurrentSourceDir
from iprm.api.project import Project, SubDir
from iprm.api.target import Target
from iprm.api.cpp import CppTarget
from iprm.api.rust import RustTarget


class SCons(BuildSystem):
    _default_alias = 'all'
    _scons_struct_file = 'SConstruct'
    _scons_script_file = 'SConscript'

    def __init__(self, native_loader: Loader, **kwargs):
        kwargs['build_dir'] = 'build'
        super().__init__(native_loader, **kwargs)

    def _generate_file_name(self):
        return self._scons_struct_file if self._is_root_item else self._scons_script_file

    @classmethod
    def generate_file_exts(cls) -> list[str]:
        return [cls._scons_struct_file, cls._scons_script_file]

    @classmethod
    def _default_build_type(cls):
        return cls._release_build_type()

    @classmethod
    def _release_build_type(cls):
        return 'release'

    @classmethod
    def _debug_build_type(cls):
        return 'debug'

    @classmethod
    def build(cls, **kwargs):
        bindir = kwargs.get('bindir')
        target = kwargs.get('target', None)
        cmd = [
            'scons',
            f'--build-dir={bindir}',
            f'--build-type={cls.build_type(**kwargs)}',
            f'-j{cls.num_procs(**kwargs)}',
        ]
        if target:
            cmd.append(target)
        platform_ctx = kwargs.get('platform_ctx')
        return cls._run_command(cmd, platform_ctx)

    @classmethod
    def current_bin_dir(cls):
        return "Path(env.Dir('.').get_path(env.Dir('.').srcnode().dir))"

    @classmethod
    def relative_src_path(cls, root_relative_path: Path, dir_path: Dir, leaf_path: str = None):
        leaf = '' if leaf_path is None else f'{cls.dir_separator()}{leaf_path}'
        prefix_dir = f'#{str(root_relative_path.as_posix())}'
        if isinstance(dir_path, CurrentSourceDir):
            return f'"{prefix_dir}{leaf}"'
        path = dir_path.path
        return f"'{prefix_dir}{cls.dir_separator()}{path.as_posix()}{leaf}'"

    # TODO: Attach custom tools to the environment to keep the SConstruct/SConscripts clean and remove the boilerplate

    def _generate_file_header(self):
        scons_content = super()._generate_file_header()
        scons_content.extend([
            'import os',
            'import platform',
            'from pathlib import Path',
        ])
        if not self._is_root_item:
            scons_content.append(
                "Import('env')",
            )
        return scons_content

    def _generate_project(self, project: Project) -> list[str]:
        scons_content = []
        options = project.properties.get('options', {})
        if options:
            # TODO: Add user specified options
            scons_content.append('')
            for opt_name, opt_config in options.items():
                opt_description = opt_config.get('description')
                opt_default = opt_config.get('default')
                opt_type = opt_config.get('type')

        scons_content.append(f"""
AddOption(
    '--build-dir',
    dest='build_dir',
    type='string',
    default='build',
    help='Specify the build output directory (default: build)'
)

AddOption(
    '--build-type',
    dest='build_type',
    type='choice',
    choices=['debug', 'release'],
    default='debug',
    help='Specify the build type: debug or release (default: debug)'
)

build_base = Path(GetOption('build_dir'))
build_type = GetOption('build_type')
build_path = build_base / build_type

env = Environment(ENV=os.environ)
env['BUILD_PATH'] = build_path

env['WINDOWS'] = platform.system() == 'Windows'
env['MACOS'] = platform.system() == 'Darwin'
env['LINUX'] = platform.system() == 'Linux'

if env['MACOS']:
    env.Replace(CC='clang', CXX='clang++')
elif env['LINUX']:
    env.Replace(CC='gcc', CXX='g++')

env['GCC'] = env['CC'] == 'gcc' and env['CXX'] == 'g++'
env['CLANG'] = env['CC'] == 'clang' and env['CXX'] == 'clang++'
env['MSVC'] = 'msvc' in env['TOOLS'] and not (env['GCC'] or env['CLANG'])
env['RELEASE'] = build_type == 'release'
env['DEBUG'] = build_type == 'debug'

env.Append(CXXFLAGS=['-std=c++20' if env['GCC'] or env['CLANG'] else '/std:c++20'])
if env['MSVC']:
    env.Append(CXXFLAGS=['/EHsc'])

if env['DEBUG']:
    if env['MSVC']:
        env.Append(
            CXXFLAGS=['/Od', '/FS'],
            LINKFLAGS=['/DEBUG'],
            CPPDEFINES=['DEBUG']
        )
    else:
        env.Append(
            CXXFLAGS=['-g', '-O0'],
            CPPDEFINES=['DEBUG']
        )
elif env['RELEASE']:
    if env['MSVC']:
        env.Append(
            CXXFLAGS=['/O2'],
            LINKFLAGS=[],
            CPPDEFINES=['NDEBUG']
        )
    else:
        env.Append(
            CXXFLAGS=['-O2'],
            CPPDEFINES=['NDEBUG']
        )

env.Alias('{SCons._default_alias}')
Default('{SCons._default_alias}')
Export('env')
""")
        return scons_content

    def _generate_subdir(self, subdir: SubDir) -> list[str]:
        scons_content = []
        in_root = subdir.path.parent == Path(self.loader.project_dir).absolute()
        dir_name = subdir.path.name
        if in_root:
            scons_content.append(
                f"env.SConscript('{dir_name}/SConscript', variant_dir= str(env['BUILD_PATH'] / '{dir_name}'), duplicate=0)")
        else:
            scons_content.append(f"env.SConscript('{dir_name}/SConscript')")
        return scons_content

    @classmethod
    def _start_target_env(cls, target: Target) -> tuple[list[str], str, str, str]:
        target_name = target.name
        target_env = f'{target_name}_env'
        target_exports = f'{target_name}_exports'
        scons_content = [f"""{target_exports} = {{
    'CPPPATH': [],
    'CPPDEFINES': [],
    'LIBPATH': [],
    'LIBS': [],
    'LINKFLAGS': [],
    'RUNTIMEPATH': [],
    'PYTHONPATH': [],
}}
{target_env} = env.Clone()"""]
        dependencies = target.dependencies
        if dependencies:
            target_imports = f'{target_name}_imports'
            for dependency in dependencies:
                target_import = f'{dependency}_exports'
                scons_content.append(f"Import('{target_import}')")
                scons_content.append(f"{dependency}_target = {target_import}.get('TARGET')")
                scons_content.append(f"""{target_env}.Append(CPPPATH={target_import}.get('CPPPATH', []))
{target_env}.Append(LIBPATH={target_import}.get('LIBPATH', []))
{target_env}.Append(LIBS={target_import}.get('LIBS', []))
{target_env}.Append(LINKFLAGS={target_import}.get('LINKFLAGS', []))""")
                if target.is_app or target.is_test:
                    # TODO: Clean this up and only add if the dependency itself is a shared library or executable
                    target_runtime_paths = f'{dependency}_runtime_paths '
                    target_python_paths = f'{dependency}_python_paths '
                    scons_content.append(f"""{target_runtime_paths} = ';'.join({target_import}.get('RUNTIMEPATH', []))
if {target_runtime_paths}:
    path_var = {target_env}['ENV'].get('PATH', '')
    if path_var:
        {target_env}['ENV']['PATH'] = {target_runtime_paths} + ';' + path_var
    else:
        {target_env}['ENV']['PATH'] = {target_runtime_paths}
{target_python_paths} = ';'.join({target_import}.get('PYTHONPATH', []))
if {target_python_paths}:
    path_var = {target_env}['ENV'].get('PYTHONPATH', '')
    if path_var:
        {target_env}['ENV']['PYTHONPATH'] = {target_python_paths} + ';' + path_var
    else:
        {target_env}['ENV']['PYTHONPATH'] = {target_python_paths}
""")
        return scons_content, target_name, target_env, target_exports

    @classmethod
    def _end_target_env(cls, target: Target) -> list[str]:
        target_name = target.name
        target_env = f'{target_name}_env'
        target_exports = f'{target_name}_exports'
        target_instance = f'{target_name}_target'
        target_instance_name = f'{target_instance}_name'
        target_isntance_dir = f'{target_instance}_dir'
        scons_content = []
        if target.is_lib:
            scons_content.extend([f"""{target_instance} = {target_name}[0]
{target_instance_name} = Path({target_instance}.name).stem
{target_isntance_dir} = str(Path({target_instance}.dir.path).as_posix())
{target_exports}['LIBPATH'].append(f'#{{{target_isntance_dir}}}')
{target_exports}['LIBS'].append({target_instance_name})"""])
        # TODO: Also support retrieving the path of an executable
        if target.is_shared:
            scons_content.append(f"{target_exports}['RUNTIMEPATH'].append(f'{{{target_isntance_dir}}}')")
        if not target.is_third_party and target.is_python:
            scons_content.append(f"""{target_instance} = {target_name}[0]
{target_instance_name} = Path({target_instance}.name).stem
{target_isntance_dir} = str(Path({target_instance}.dir.path).as_posix())
{target_exports}['PYTHONPATH'].append(f'{{{target_isntance_dir}}}')""")
        scons_content.append(f"""{target_exports}['CPPPATH'].extend({target_env}.get('CPPPATH', []))
{target_exports}['TARGET'] = {target_name}
env.Alias('{target_name}', {target_name})
env.Alias('all', {target_name})
Export('{target_exports}')
""")
        return scons_content

    def _generate_target(self, target: Target) -> list[str]:
        pass

    def _generate_cpp(self, cpp: CppTarget):
        first_party = not cpp.is_third_party
        if first_party:
            return self._generate_cpp_first_party(cpp)
        else:
            return self._generate_cpp_third_party(cpp)

    def _generate_cpp_first_party(self, cpp: CppTarget):
        scons_content, target_name, target_env, target_exports = self._start_target_env(cpp)
        root_relative_path = cpp.root_relative_dir.path
        include_paths = cpp.properties.get('include_paths')
        if include_paths:
            scons_content.append(f'{target_env}.Append(')
            scons_content.append('\tCPPPATH=[')
            for include_path in include_paths:
                scons_content.append(f'\t\t{self.relative_src_path(root_relative_path, include_path)},')
            scons_content.append('\t]')
            scons_content.append(')')

        if cpp.is_app or cpp.is_test:
            scons_content.append(f'{target_name} = {target_env}.Program(')
        elif cpp.is_static:
            scons_content.append(f'{target_name} = {target_env}.StaticLibrary(')
        elif cpp.is_shared:
            scons_content.append(f'{target_name} = {target_env}.SharedLibrary(')
        elif cpp.is_python:
            scons_content.append(f'{target_name} = {target_env}.SharedLibrary(')
            scons_content.append("\tSHLIBPREFIX='',")
        else:
            # If we didn't recognize/support the type, don't generate any content
            return scons_content
        suffix = cpp.properties.get('suffix', '')
        if suffix:
            suffix = f'.{suffix}' if not suffix.startswith('.') else suffix
            scons_content.append(f"\tSHLIBSUFFIX='{suffix}',")
        scons_content.append(f"\ttarget='{target_name}',")
        sources_dict = cpp.properties.get('sources', {})
        if sources_dict:
            scons_content.append('\tsource=[')
            for src_dir, src_files in sources_dict.items():
                for src_file in src_files:
                    scons_content.append(f"\t\t'{(src_dir.path / src_file).as_posix()}',")
            scons_content.append('\t],')
        scons_content.append(f'\t{self._cpp_add_pdb(cpp)}')
        scons_content.append(')')

        dependencies = cpp.dependencies
        if dependencies:
            imported_targets = f'{target_name}_imported_targets'
            scons_content.append(f'{imported_targets} = [')
            for dependency in dependencies:
                scons_content.append(f'\t{dependency}_target,')
            scons_content.append(']')
            scons_content.append(f"""for source in {target_name}[0].sources:
    {target_env}.Depends({target_env}.File(str(source)), {imported_targets})""")

        if cpp.is_python:
            scons_content.extend(self._add_python_dependency(cpp))

        if cpp.is_app or cpp.is_test:
            target_post_action_commands = f'{target_name}_post_action_commands'
            scons_content.append(f'{target_post_action_commands} = []')
            if cpp.is_test:
                scons_content.append(f"{target_post_action_commands}.append('cmd /C $TARGET' if platform.system() == 'Windows' else './$TARGET')")
            scons_content.append(f"""if {target_post_action_commands}:
        {target_env}.AddPostAction({target_name}, {target_post_action_commands})
    """)

        scons_content.extend(self._end_target_env(cpp))
        scons_content.append('')
        return scons_content

    @staticmethod
    def _add_python_dependency(cpp: CppTarget):
        # TODO: Create a tool for this and centralize it
        target_name = cpp.name
        target_env = f'{target_name}_env'
        return [f"""def find_python({target_env}, version=None):
    import sys, subprocess, os, glob
    result = {{
        'FOUND': False,
        'INCLUDE_DIR': None,
        'LIBRARY_DIR': None,
        'LIBRARY': None,
        'VERSION': None,
        'EXECUTABLE': None,
        'FRAMEWORK_PATH': None,
        'LINKFLAGS': []
    }}

    try:
        result['EXECUTABLE'] = sys.executable
        result['VERSION'] = f"{{sys.version_info.major}}.{{sys.version_info.minor}}.{{sys.version_info.micro}}"

        if version and not version.startswith(f"{{sys.version_info.major}}.{{sys.version_info.minor}}"):
            print(f"Warning: Requested Python version {{version}} but found {{result['VERSION']}}")

        py_cmd = [
            sys.executable,
            "-c",
            "import sysconfig; print(sysconfig.get_path('include'))"
        ]
        result['INCLUDE_DIR'] = subprocess.check_output(py_cmd).decode().strip()

        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        
        if {target_env}['MACOS']:
            is_homebrew = False
            homebrew_prefix = None
            if '/homebrew/' in sys.executable.lower() or '/brew/' in sys.executable.lower():
                is_homebrew = True
                homebrew_parts = sys.executable.split('/bin/python')
                if homebrew_parts:
                    homebrew_prefix = homebrew_parts[0]
            
            if not is_homebrew and in_venv:
                py_cmd = [
                    sys.executable,
                    "-c",
                    "import sys; " +
                    "base_prefix = getattr(sys, 'real_prefix', getattr(sys, 'base_prefix', sys.prefix)); " +
                    "print(base_prefix)"
                ]
                base_prefix = subprocess.check_output(py_cmd).decode().strip()
                if '/homebrew/' in base_prefix.lower() or '/brew/' in base_prefix.lower():
                    is_homebrew = True
                    homebrew_prefix = base_prefix
            
            if is_homebrew:
                framework_candidates = [
                    f"{{homebrew_prefix}}/Frameworks/Python.framework",
                    f"{{homebrew_prefix}}/opt/python@{{sys.version_info.major}}.{{sys.version_info.minor}}/Frameworks/Python.framework",
                    "/opt/homebrew/Frameworks/Python.framework",
                    f"/opt/homebrew/opt/python@{{sys.version_info.major}}.{{sys.version_info.minor}}/Frameworks/Python.framework"
                ]
                
                for framework_path in framework_candidates:
                    if os.path.exists(framework_path):
                        version_specific_path = os.path.join(framework_path, f"Versions/{{sys.version_info.major}}.{{sys.version_info.minor}}")
                        if os.path.exists(version_specific_path):
                            python_binary = os.path.join(version_specific_path, "Python")
                            if os.path.exists(python_binary):
                                print(f"Found Homebrew Python framework at: {{framework_path}}")
                                result['FRAMEWORK_PATH'] = framework_path
                                
                                # For Homebrew Python, we need to link directly with the framework
                                framework_dir = os.path.dirname(framework_path)
                                result['LINKFLAGS'] = [
                                    f"-F{{framework_dir}}",
                                    "-framework", "Python"
                                ]
                                result['FOUND'] = True
                                break
            if not result['FOUND']:
                framework_candidates = [
                    "/Library/Frameworks/Python.framework",
                    "/System/Library/Frameworks/Python.framework",
                    "/usr/local/Frameworks/Python.framework"
                ]
                
                for framework_path in framework_candidates:
                    version_path = os.path.join(framework_path, f"Versions/{{sys.version_info.major}}.{{sys.version_info.minor}}")
                    if os.path.exists(version_path):
                        python_binary = os.path.join(version_path, "Python")
                        if os.path.exists(python_binary):
                            print(f"Found system Python framework at: {{framework_path}}")
                            result['FRAMEWORK_PATH'] = framework_path
                            framework_dir = os.path.dirname(framework_path)
                            result['LINKFLAGS'] = [
                                f"-F{{framework_dir}}",
                                "-framework", "Python"
                            ]
                            result['FOUND'] = True
                            break
            
            if not result['FOUND']:
                try:
                    py_cmd = [
                        sys.executable,
                        "-c",
                        "import sysconfig; " +
                        "print(sysconfig.get_config_var('PYTHONFRAMEWORKPREFIX') or '')"
                    ]
                    framework_prefix = subprocess.check_output(py_cmd).decode().strip()
                    
                    if framework_prefix:
                        py_cmd = [
                            sys.executable,
                            "-c",
                            "import sysconfig; " +
                            "print(sysconfig.get_config_var('PYTHONFRAMEWORKDIR') or '')"
                        ]
                        framework_dir = subprocess.check_output(py_cmd).decode().strip()
                        
                        if framework_dir and framework_dir != "no-framework":
                            framework_path = os.path.join(framework_prefix, "Python.framework")
                            if os.path.exists(framework_path):
                                version_path = os.path.join(framework_path, f"Versions/{{sys.version_info.major}}.{{sys.version_info.minor}}")
                                if os.path.exists(version_path):
                                    python_binary = os.path.join(version_path, "Python")
                                    if os.path.exists(python_binary):
                                        print(f"Found Python framework using sysconfig at: {{framework_path}}")
                                        result['FRAMEWORK_PATH'] = framework_path
                                        result['LINKFLAGS'] = [
                                            f"-F{{framework_prefix}}",
                                            "-framework", "Python"
                                        ]
                                        result['FOUND'] = True
                except Exception as e:
                    print(f"Error getting framework info from Python: {{e}}")
            
            if not result['FOUND']:
                potential_dirs = [
                    "/opt/homebrew/opt",
                    "/usr/local/opt",
                    "/Library/Frameworks"
                ]
                
                for base_dir in potential_dirs:
                    if os.path.exists(base_dir):
                        python_dirs = glob.glob(f"{{base_dir}}/python@{{sys.version_info.major}}.{{sys.version_info.minor}}*")
                        for py_dir in python_dirs:
                            # Check for framework structure
                            frameworks_dir = os.path.join(py_dir, "Frameworks")
                            if os.path.exists(frameworks_dir):
                                python_framework = os.path.join(frameworks_dir, "Python.framework")
                                if os.path.exists(python_framework):
                                    version_dir = os.path.join(python_framework, f"Versions/{{sys.version_info.major}}.{{sys.version_info.minor}}")
                                    if os.path.exists(version_dir):
                                        python_binary = os.path.join(version_dir, "Python")
                                        if os.path.exists(python_binary):
                                            print(f"Found Python framework by directory search: {{python_framework}}")
                                            result['FRAMEWORK_PATH'] = python_framework
                                            result['LINKFLAGS'] = [
                                                f"-F{{frameworks_dir}}",
                                                "-framework", "Python"
                                            ]
                                            result['FOUND'] = True
                                            break
        
        elif {target_env}['WINDOWS']:
            if in_venv:
                py_cmd = [
                    sys.executable,
                    "-c",
                    "import sys, os; " +
                    "base_prefix = getattr(sys, 'real_prefix', getattr(sys, 'base_prefix', sys.prefix)); " +
                    "print(os.path.join(base_prefix, 'libs'))"
                ]
            else:
                py_cmd = [
                    sys.executable,
                    "-c",
                    "import sys, os; print(os.path.join(os.path.dirname(sys.executable), 'libs'))"
                ]
            result['LIBRARY_DIR'] = subprocess.check_output(py_cmd).decode().strip()
            result['LIBRARY'] = f"python{{sys.version_info.major}}{{sys.version_info.minor}}"
            
            lib_file = os.path.join(result['LIBRARY_DIR'], f"{{result['LIBRARY']}}.lib")
            if os.path.exists(lib_file):
                result['FOUND'] = True
            else:
                print(f"Warning: Python library {{lib_file}} not found.")

        else:
            if in_venv:
                py_cmd = [
                    sys.executable,
                    "-c",
                    "import sys, sysconfig, os; " +
                    "base_prefix = getattr(sys, 'real_prefix', getattr(sys, 'base_prefix', sys.prefix)); " +
                    "print(os.path.join(base_prefix, 'lib'))"
                ]
                base_lib_dir = subprocess.check_output(py_cmd).decode().strip()

                py_arch_cmd = [
                    sys.executable,
                    "-c",
                    "import sysconfig; print(sysconfig.get_config_var('MULTIARCH') or '')"
                ]
                multiarch = subprocess.check_output(py_arch_cmd).decode().strip()

                lib_candidates = [
                    base_lib_dir,  # /usr/lib
                    os.path.join(base_lib_dir, multiarch),  # /usr/lib/x86_64-linux-gnu
                    os.path.join(base_lib_dir, f"python{{sys.version_info.major}}.{{sys.version_info.minor}}"),  # /usr/lib/python3.x
                    os.path.join(base_lib_dir, f"python{{sys.version_info.major}}.{{sys.version_info.minor}}", "config")  # /usr/lib/python3.x/config
                ]

                lib_name = f"python{{sys.version_info.major}}.{{sys.version_info.minor}}"
                lib_pattern = f"lib{{lib_name}}*.so"  # The .so files or symlinks

                for lib_dir in lib_candidates:
                    if os.path.exists(lib_dir):
                        # Check if this directory contains the Python library
                        lib_files = glob.glob(os.path.join(lib_dir, lib_pattern))
                        if lib_files:
                            result['LIBRARY_DIR'] = lib_dir
                            break
                            
                if not result['LIBRARY_DIR'] and result['INCLUDE_DIR']:
                    include_components = result['INCLUDE_DIR'].split(os.sep)
                    if len(include_components) >= 3:
                        base_components = include_components[:-2]  # Remove 'include/pythonX.Y'
                        lib_dir = os.path.join(os.sep, *base_components, 'lib', include_components[-1])
                        if os.path.exists(lib_dir):
                            result['LIBRARY_DIR'] = lib_dir
            else:
                py_cmd = [
                    sys.executable,
                    "-c",
                    "import sysconfig; " +
                    "print(sysconfig.get_config_var('LIBDIR') or sysconfig.get_config_var('LIBPL'))"
                ]
                result['LIBRARY_DIR'] = subprocess.check_output(py_cmd).decode().strip()

            if not result['LIBRARY_DIR'] or not os.path.exists(result['LIBRARY_DIR']):
                py_cmd = [
                    sys.executable,
                    "-c",
                    "import sysconfig; " +
                    "from distutils.sysconfig import get_config_var; " +
                    "print(get_config_var('LIBPL'))"
                ]
                result['LIBRARY_DIR'] = subprocess.check_output(py_cmd).decode().strip()

            py_cmd = [
                sys.executable,
                "-c",
                "import sysconfig; " +
                "print(sysconfig.get_config_var('LIBRARY') or " +
                f"'python{{sys.version_info.major}}.{{sys.version_info.minor}}')"
            ]
            lib = subprocess.check_output(py_cmd).decode().strip()
            if lib.startswith('lib'):
                lib = lib[3:]
            if lib.endswith('.a'):
                lib = lib[:-2]
            result['LIBRARY'] = lib
            
            lib_file_so = os.path.join(result['LIBRARY_DIR'], f"lib{{result['LIBRARY']}}.so")
            lib_file_a = os.path.join(result['LIBRARY_DIR'], f"lib{{result['LIBRARY']}}.a")
            
            if os.path.exists(lib_file_so) or os.path.exists(lib_file_a):
                result['FOUND'] = True
            else:
                print(f"Warning: Python library not found in {{result['LIBRARY_DIR']}}")

    except Exception as e:
        print(f"Error finding Python: {{e}}")
        import traceback
        traceback.print_exc()

    return result
    
python_info = find_python({target_env})
print(f"Python detection results: FOUND={{python_info['FOUND']}}, VERSION={{python_info['VERSION']}}")

if python_info['FOUND']:
    if python_info['INCLUDE_DIR'] and os.path.exists(python_info['INCLUDE_DIR']):
        {target_env}.Append(CPPPATH=[python_info['INCLUDE_DIR']])
    
    if {target_env}['MACOS'] and python_info['LINKFLAGS']:
        {target_env}.Append(LINKFLAGS=python_info['LINKFLAGS'])
    elif python_info['LIBRARY_DIR'] and python_info['LIBRARY']:
        {target_env}.Append(
            LIBPATH=[python_info['LIBRARY_DIR']],
            LIBS=[python_info['LIBRARY']]
        )
    
    major, minor, micro = [int(x) for x in python_info['VERSION'].split('.')]
    {target_env}.Append(
        CPPDEFINES=[
            ('PY_MAJOR_VERSION', major),
            ('PY_MINOR_VERSION', minor),
            ('PY_MICRO_VERSION', micro)
        ]
    )
else:
    print("ERROR: Could not find Python libraries!")"""]

    def _generate_cpp_third_party(self, cpp: CppTarget):
        scons_content = []
        # TODO: Implement all third party types
        if cpp.is_imported:
            pass
        elif cpp.is_source_archive:
            pass
        elif cpp.is_precompiled_archive:
            pass
        elif cpp.is_git:
            scons_content.extend(self._generate_cpp_third_party_git(cpp))
        elif cpp.is_homebrew:
            pass
        elif cpp.is_pkgconfig:
            pass
        elif cpp.is_system:
            pass
        return scons_content

    def _generate_cpp_third_party_git(self, cpp: CppTarget):
        scons_content, target_name, target_env, target_exports = self._start_target_env(cpp)
        target_git = f'{target_name}_git'
        target_git_clone_path = f'{target_git}_clone_path'
        target_git_clone_marker = f'{target_name}_marker'
        scons_content.append(f"{target_git_clone_path} = {self.current_bin_dir()}")
        include_paths = cpp.properties.get('include_paths')
        if include_paths:
            scons_content.append(f'{target_env}.Append(')
            scons_content.append('\tCPPPATH=[')
            for include_path in include_paths:
                scons_content.append(f"\t\t{target_git_clone_path} / '{str(include_path.path.as_posix())}',")
            scons_content.append('\t]')
            scons_content.append(')')

        # TODO: Move this to a custom tool that gets registered with the base environment
        scons_content.append(f"""import subprocess
import SCons.Action
import SCons.Builder

{target_git_clone_marker} = '.clone_complete'

def clone_git_repository(target, source, env):
    dest_dir = str(env['DEST_DIR'])
    tag = env['GIT_TAG']
    repository = env['GIT_REPO']
    subprocess.check_call([
        'git',
        'clone',
        '--depth',
        '1',
        '--branch',
        tag,
        repository,
        dest_dir,
    ])
    import time
    with open(str(target[0]), 'w') as f:
        f.write(f"Git clone of {{repository}} at tag {{tag}} completed at {{time.time()}}")
    return None

def check_git_repository(target, source, env):
    dest_dir = str(env['DEST_DIR'])
    if os.path.exists(dest_dir) and os.path.isdir(dest_dir) and len(os.listdir(dest_dir)) > 0:
        return None
    return 1

git_cloner = SCons.Builder.Builder(
    action=SCons.Action.Action(
        clone_git_repository,
        "Cloning $GIT_REPO into $TARGET"
    ),
    source_scanner=SCons.Scanner.Scanner(function=check_git_repository)
)
{target_env}.Append(BUILDERS={{'GitRepository': git_cloner}})
""")

        tag = cpp.properties.get('git_tag')
        repository = cpp.properties.get('git_repository')

        target_git = target_name if cpp.is_header else target_git
        scons_content.append(f'{target_git} = {target_env}.GitRepository(')
        scons_content.append(f"\ttarget={target_git_clone_marker},")
        scons_content.append(f'\tsource=None,')
        scons_content.append(f"\tGIT_TAG='{tag}',")
        scons_content.append(f"\tGIT_REPO='{repository}',")
        scons_content.append(f"\tDEST_DIR={target_git_clone_path} / '_git',")
        scons_content.append(')')
        if not cpp.is_header:
            scons_content.append(f"env.Alias('{target_git}', {target_git})")
            scons_content.append(f"env.Alias('all', {target_git})")

        if cpp.is_static:
            sources_dict = cpp.properties.get('sources', {})
            target_sources = f'{target_name}_sources'
            scons_content.append(f'{target_sources} = [')
            if sources_dict:
                for src_dir, src_files in sources_dict.items():
                    for src_file in src_files:
                        scons_content.append(
                            f"\t{target_env}.File({target_git_clone_path} / '{(src_dir.path / src_file).as_posix()}'),")
                scons_content.append(']')
            else:
                scons_content[-1] += ']'
            scons_content.append(f"""for source in {target_sources}:
    {target_env}.Depends(source, {target_git})
""")
            scons_content.append(f'{target_name} = {target_env}.StaticLibrary(')
            scons_content.append(f"\ttarget='{target_name}',")
            scons_content.append(f'\tsource={target_sources},')
            scons_content.append(f'\t{self._cpp_add_pdb(cpp)}')
            scons_content.append(')')

        # TODO: Impl app, test, shared, and python

        scons_content.extend(self._end_target_env(cpp))
        scons_content.append('')
        return scons_content

    def _cpp_add_pdb(self, cpp: CppTarget):
        target_name = cpp.name
        target_env = f'{target_name}_env'
        return f"PDB='{target_name}.pdb' if {target_env}['MSVC'] and {target_env}['DEBUG'] else None"

    def _generate_rust(self, rust: RustTarget) -> list[str]:
        pass
