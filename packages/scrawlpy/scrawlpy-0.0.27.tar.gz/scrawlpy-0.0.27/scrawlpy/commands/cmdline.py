# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/20 10:37
@Author  : jayden
"""

import re
import sys
from os.path import dirname, join
import os

import requests

from scrawlpy.commands import create_builder
from scrawlpy.commands import retry
from scrawlpy.commands import shell
from scrawlpy.commands import zip

HELP = """

Version: {version}
Document:

Usage:
  scrawlpy <command> [options] [args]
      
Available commands:
"""

NEW_VERSION_TIP = """
──────────────────────────────────────────────────────
New version available \033[31m{version}\033[0m → \033[32m{new_version}\033[0m
Run \033[33mpip install --upgrade scrawlpy\033[0m to update!
"""

about = {}
here = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
with open(os.path.join(here, "scrawlpy", "__version__.py"), mode="r", encoding="utf-8") as f:
    exec(f.read(), about)
VERSION = about["__version__"]


def _print_commands():
    print(HELP.rstrip().format(version=VERSION))
    cmds = {
        "create": "create project、spider、item and so on",
        "shell": "debug response",
        "zip": "zip project",
        "retry": "retry failed request or item",
    }
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass))

    print('\nUse "scrawlpy <command> -h" to see more info about a command')


def check_new_version():
    try:
        url = "https://pypi.org/simple/scrawlpy/"
        resp = requests.get(url, timeout=3, verify=False)
        html = resp.text

        last_stable_version = re.findall(r"scrawlpy-([\d.]*?).tar.gz", html)[-1]
        now_version = VERSION
        now_stable_version = re.sub("-beta.*", "", VERSION)

        if now_stable_version < last_stable_version or (
                now_stable_version == last_stable_version and "beta" in now_version
        ):
            new_version = f"scrawlpy=={last_stable_version}"
            if new_version:
                version = f"scrawlpy=={VERSION.replace('-beta', 'b')}"
                tip = NEW_VERSION_TIP.format(version=version, new_version=new_version)
                # 修复window下print不能带颜色输出的问题
                if os.name == "nt":
                    os.system("")
                print(tip)
    except Exception as e:
        pass


def execute():
    try:
        args = sys.argv
        if len(args) < 2:
            _print_commands()
            check_new_version()
            return

        command = args.pop(1)
        if command == "create":
            create_builder.main()
        elif command == "shell":
            shell.main()
        elif command == "zip":
            zip.main()
        elif command == "retry":
            retry.main()
        else:
            _print_commands()
    except KeyboardInterrupt:
        pass

    check_new_version()


if __name__ == "__main__":
    execute()
