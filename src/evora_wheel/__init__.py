#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-05-05
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

# isort:skip_file

from __future__ import annotations
import logging

from typing import cast
import pkg_resources


NAME = "evora-wheel"

__version__ = pkg_resources.get_distribution(NAME).version


from .dummy import EvoraFilterWheelDummy
from .wheel import EvoraFilterWheel

from .server import EvoraWheelServer
