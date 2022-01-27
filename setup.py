#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""


from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')


setup(
    maintainer='Xdev',
    maintainer_email='xdev@ucar.edu',
    description='xpersist provides custom caching utility functions in Python',
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
    ],
    license='Apache Software License 2.0',
    long_description_content_type='text/markdown',
    long_description=long_description,
    name='xpersist',
    packages=find_packages(),
    url='https://github.com/ncar-xdev/xpersist',
    project_urls={
        'Documentation': 'https://github.com/ncar-xdev/xpersist',
        'Source': 'https://github.com/ncar-xdev/xpersist',
        'Tracker': 'https://github.com/ncar-xdev/xpersist/issues',
    },
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
    zip_safe=False,
)
