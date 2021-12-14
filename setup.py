#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""


from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')


setup(
    maintainer='Xdev',
    maintainer_email='xdev@ucar.edu',
    description='xpersist provides custom caching utility functions in Python',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description_content_type='text/markdown',
    long_description=long_description,
    name='xpersist',
    packages=['xpersist'],
    url='https://github.com/NCAR/xpersist',
    project_urls={
        'Documentation': 'https://github.com/NCAR/xpersist',
        'Source': 'https://github.com/NCAR/xpersist',
        'Tracker': 'https://github.com/NCAR/xpersist/issues',
    },
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
    zip_safe=False,
)
