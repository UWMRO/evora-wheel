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

from sdsstools.logger import get_logger
from sdsstools.metadata import get_package_version


NAME = "evora-wheel"

log = get_logger(NAME)
log.sh.setLevel(logging.INFO)
__version__ = cast(str, get_package_version(path=__file__, package_name=NAME))


from .dummy import EvoraFilterWheelDummy
from .wheel import EvoraFilterWheel

from .server import EvoraWheelServer
