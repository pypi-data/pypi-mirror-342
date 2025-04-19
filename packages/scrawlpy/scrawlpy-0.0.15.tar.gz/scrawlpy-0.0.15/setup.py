# -*- coding: utf-8 -*-
"""
Created on 2020/4/22 10:45 PM
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""

from os.path import dirname, join
from sys import version_info

import setuptools

if version_info < (3, 6, 0):
    raise SystemExit("Sorry! scrawlpy requires python 3.6.0 or later.")

with open(join(dirname(__file__), "scrawlpy/VERSION"), "r") as fh:
    version = fh.read().strip()

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()
packages.extend(
    [
        "scrawlpy",
        # "scrawlpy.templates",
        # "scrawlpy.templates.project_template",
        # "scrawlpy.templates.project_template.spiders",
        # "scrawler.templates.project_template.items",
    ]
)

requires = [
    "requests>=2.22.0",
]

render_requires = [
    "webdriver-manager>=4.0.0",
    "playwright",
    "selenium>=3.141.0",
]

all_requires = [
    "bitarray>=1.5.3",
    "PyExecJS>=1.5.1",
    "pymongo>=3.10.1",
    "redis-py-cluster>=2.1.0",
] + render_requires

setuptools.setup(
    name="scrawlpy",
    version=version,
    author="Jayden",
    license="MIT",
    author_email="jayden@qq.com",
    python_requires=">=3.6",
    description="scrawlpy是一款python爬虫框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requires,
    extras_require={"all": all_requires, "render": render_requires},
    entry_points={"console_scripts": ["scrawlpy = scrawlpy.commands.cmdline:execute"]},
    # url="https://github.com/Boris-code/feapder.git",
    packages=packages,
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
