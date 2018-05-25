#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requires = [
    'requests>=2.18.0'
]

test_requires = [
    'pytest',
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
    version='7.5.0b1',
    packages=['necbaas'],
    description='NEC Mobile Backend platform Python SDK',
    author='NEC Corporation',
    url='http://jpn.nec.com/iot/platform/iotpfservice',
    install_requires=requires,
    extra_requires={
        'test': test_requires,
        'doc': doc_requires
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)

