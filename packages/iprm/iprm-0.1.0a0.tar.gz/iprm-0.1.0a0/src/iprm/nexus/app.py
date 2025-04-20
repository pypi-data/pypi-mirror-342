"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="IPRM Nexus")
    # TODO: define CLI, should have a mode to launch the main web server, and then launch the workers that attach
    #  themselves to a web server

    # TODO: IPRM Nexus should actually just be a full python implementation. IPRM Studio is simply a client

    parser.parse_args()


if __name__ == '__main__':
    main()
