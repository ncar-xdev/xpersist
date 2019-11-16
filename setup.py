#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup
from os.path import exists

if exists('README.md'):
    with open('README.md') as f:
        long_description = f.read()
else:
    long_description = ''

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

test_requirements = ['pytest']

setup(
    maintainer='xdev',
    maintainer_email='xdev@ucar.edu',
    description='xpersist',
    install_requires=install_requires,
    license='Apache License 2.0',
    long_description=long_description,
    name='xpersist',
    packages=['xpersist'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/matt-long/xpersist',
    zip_safe=False,
)
