#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
from codecs import open

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

here = os.path.abspath(os.path.dirname(__file__))

about = {}
try:
    with open(os.path.join(here, 'necbaas', '__version__.py'), encoding="utf-8") as f:
        exec(f.read(), about)

    with open("Description.rst", encoding="utf-8") as f:
        description = f.read()
except IOError:
    # for tox
    description = "dummy description"

setup(
    name='necbaas',
    version=about['__version__'],
    packages=['necbaas'],
    description='NEC Mobile Backend platform Python SDK',
    long_description=description,
    author='NEC Corporation',
    url='https://nec-baas.github.io/',
    install_requires=requires,
    extras_require={
        'test': test_requires,
        'doc': doc_requires
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)

