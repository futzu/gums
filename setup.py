#!/usr/bin/env python3

import setuptools
import gumd

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="gumd",
    version=gumd.version(),
    author="Adrian",
    author_email="spam@iodisco.com",
    description="gumd, Grande Unified Multicast Daemon",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/gumd",
    install_requires=[
        "new_reader >=0.1.07",
    ],
    py_modules=["gumd","gumc"],
    scripts=['bin/gumd', 'bin/gumc'],
    platforms="all",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.6",
)
