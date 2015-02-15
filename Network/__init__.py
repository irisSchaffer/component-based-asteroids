# Game Architecture Network Layer
#
# Copyright (c) 2014 Roman Divotkey, Univ. of Applied Sciences Upper Austria. 
# All rights reserved.
#
# This file is subject to the terms and conditions defined in file
# 'LICENSE', which is part of this source code package.
#
# THIS CODE IS PROVIDED AS EDUCATIONAL MATERIAL AND NOT INTENDED TO ADDRESS
# ALL REAL WORLD PROBLEMS AND ISSUES IN DETAIL.

"""Basic network layer for Python-based network games.
The intended purpose of this package is to be used as lecture material and
boilerplate for network games and interactive application written in Python.

This package is provided as educational material and not indented to
address all real world problems and issues in detail.
"""

import imp

from . import network
from . import xprotocol

def _version():
    try:
        imp.find_module('pkg_resources')
        from pkg_resources import get_distribution
        dist = get_distribution('ganet')
        version = dist.version
    except:
        version = 'version unknown'

    return version

__version__ = _version()
