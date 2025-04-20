#!/usr/bin/env python
# coding: utf-8

import argparse
from pathlib import Path

from .aipy.config import SETTINGS_FILES

def mainw():
    def parse_args():
        parser = argparse.ArgumentParser(description="Python use - AIPython")
        parser.add_argument("-c", '--config', type=str, default="aipy.toml")
        parser.add_argument('cmd', nargs='?', default=None, help="Task to execute, e.g. 'Who are you?'")
        return parser.parse_args()

    args = parse_args()

    try:
        import wx
    except:
        import sys
        import subprocess

        cp = subprocess.run([sys.executable, "-m", "pip", "install", 'wxpython'])
        assert cp.returncode == 0

    from .wxgui import main as aipy_main
    aipy_main(args)

def main():
    settings_files_help = "\n".join(map(str, SETTINGS_FILES))
    config_help_message = (
        f"Toml config file. If not provided, searches in:\n{settings_files_help}"
    )

    def parse_args():
        parser = argparse.ArgumentParser(description="Python use - AIPython", formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-c", '--config', type=str, default="aipy.toml", help=config_help_message)
        parser.add_argument('-p', '--python', default=False, action='store_true', help="Python mode")
        parser.add_argument('cmd', nargs='?', default=None, help="Task to execute, e.g. 'Who are you?'")
        return parser.parse_args()

    args = parse_args()

    if args.python:
        from .main import main as aipy_main
    else:
        from .saas import main as aipy_main
    aipy_main(args)

if __name__ == '__main__':
    main()
