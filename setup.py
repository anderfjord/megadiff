#!/usr/bin/env python

from setuptools import setup

setup(
    name='megadiff',
    version='0.0.12',
    url='https://github.com/anderfjord/megadiff.git',
    author='Andrew Forth',
    author_email='zanderfjord+github@gmail.com',
    license='MIT',
    packages=[
        'megadiff',
    ],
    scripts=[
        'bin/megadiff',
    ],
    install_requires=[],
    description='A simple utility to compare the contents of two massive files',
    classifiers=[
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
    ]
)
