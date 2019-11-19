#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from os.path import exists

from setuptools import setup

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
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
    setup_requires=['setuptools_scm', 'setuptools>=30.3.0'],
    zip_safe=False,
)
