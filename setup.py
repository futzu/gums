#!/usr/bin/env python3

import setuptools
import gums

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="gums",
    version=gums.version(),
    author="Adrian",
    author_email="spam@iodisco.com",
    description="gums, Grande Unicast Multicast Sender",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/gums",
    install_requires=[
        "new_reader >=0.1.9",
    ],
    py_modules=["gums","gumc"],
    scripts=['bin/gums', 'bin/gumc'],
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
