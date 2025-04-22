"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import os
import subprocess
import sys


def run_command(command, env):
    try:
        subprocess.check_call(command, env=env)
    except subprocess.CalledProcessError as e:
        print(f'Error executing command {command}: {e.stderr}')
        sys.exit(1)


def main():
    studio_dir_path = os.path.dirname(__file__)
    studio_bin_dir_dir = os.path.join(studio_dir_path, 'bin')
    studio_executable = os.path.join(studio_bin_dir_dir, 'iprm_studio')
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([env.get('PYTHONPATH', ''), os.path.join(studio_dir_path, '..', '..')])
    run_command([studio_executable, *sys.argv[1:]], env=env)


if __name__ == '__main__':
    main()
