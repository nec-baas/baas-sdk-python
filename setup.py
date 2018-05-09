#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requires = [
    'requests>=2.18.0'
]

test_requires = [
    'nose',
    'mock',
    'pyyaml',
    'tox',
    'coverage'
]

doc_requires = [
    'sphinx',
    'sphinx-rtd-theme'
]

setup(
    name='necbaas',
    version='0.0.2',
    packages=['necbaas'],
    description='NEC Mobile Backend platform Python SDK',
    author='NEC Corporation',
    install_requires=requires,
    extra_requires={
        'test': test_requires,
        'doc': doc_requires
    }
)

