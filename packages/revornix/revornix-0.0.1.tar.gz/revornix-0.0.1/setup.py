#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

with open("./README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

with open("./LICENSE", "r", encoding="utf-8") as fp:
    license = fp.read()

setup(
    name = "revornix",
	version = "0.0.1",
	author = "Kinda Hall",
	author_email = "1142704468@qq.com",
	platforms = "any",
    keywords=["pip", "tools"],
    description="The python lib for revornix project",
    entry_points={
        'console_scripts': [
            'revornix = bin.main:app'
        ]
    },
    python_requires='>=3.10',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=[license],
    url="https://github.com/Alndaly/revornix-python-lib",
    maintainer="Kinda Hall",
    maintainer_email="1142704468@qq.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['typer', 'httpx', 'tqdm']
)
