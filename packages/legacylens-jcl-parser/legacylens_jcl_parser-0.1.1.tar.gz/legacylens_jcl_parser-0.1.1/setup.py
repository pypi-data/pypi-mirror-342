#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="legacylens_jcl_parser",
    version="0.1.0",
    author="Samuel Dion",
    author_email="sam94dion@gmail.com",
    description="A parser for JCL (Job Control Language) files with JSON output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samdion1994/legacylens",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "legacylens-jcl-parser=jcl_parser.cli:main",
        ],
    },
)