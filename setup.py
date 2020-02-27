# -*- coding:utf-8 -*-
""" Setup script for chipless Reader. """
import platform
from os import path
from setuptools import setup, find_packages, Extension
from codecs import open

# !/usr/bin/python
# Python:   3.6.5
# Platform: Windows/Linux/MacOS
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Impinj R2000.
# History:  2020-02-18 Wheel Ver:1.0 [Heyn] Initialization

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description = long_description.replace('\r', '')

setup(
    name='pyImpinj',
    version='1.2',

    description='Library for Impinj R2000 Reader',
    long_description=long_description,

    url='https://github.com/hex-in/pyImpinj',
    author='Heyn',
    author_email='heyunhuan@gmail.com',

    license='GPLv3',
    platforms='any',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    include_package_data=True,

    keywords=['Impinj', 'R2000'],
    packages=['pyImpinj'],

    install_requires=[ 'pyserial >= 3.4', 'libscrc == 0.1.6' ],

)
