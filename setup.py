# -*- coding: utf-8 -*-
"""
netconv setup.

Authors:  Chia-Hung Yang <yang.chi@husky.neu.edu>
          Leonardo Torres <leo@leotrs.com>
          Stefan McCabe <mccabe.s@husky.neu.edu>
          Jean-Gabriel Young <jgyou@umich.edu>
"""
from distutils.core import setup
from setuptools import find_packages
import netconv

setup(
    name=netconv.__name__,
    version=netconv.__version__,
    description=netconv.__desc__,
    author=",".join(netconv.__authors__),
    author_email=netconv.__contact__,
    packages=find_packages(),
)
