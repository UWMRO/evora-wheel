#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-05-05
# @Filename: dummy.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from time import sleep

from typing import Any

from .wheel import FilterWheelError


__all__ = ["EvoraFilterWheelDummy"]


class EvoraFilterWheelDummy:
    """A mock version of the filter wheel."""

    def __init__(self):
        self.raise_error: bool = False
        self._filterPos = None

        self.home()

    def __getattribute__(self, __name: str) -> Any:
        if object.__getattribute__(self, "raise_error") is True:
            raise FilterWheelError()

        return object.__getattribute__(self, __name)

    def home(self):
        """Homes the filter wheel."""

        sleep(5)

        self._filterPos = 0
        return True

    def getFilterPos(self):
        "Returns the position of the filterwheel, an integer between 0 and 5."

        return self._filterPos

    def moveFilter(self, num):
        "Moves the filter to the specified position, an integer between 0 and 5."

        if self._filterPos is None:
            self.home()

        if num < 0 or num > 5:
            raise FilterWheelError("Invalid filter position.")

        sleep(5)

        self._filterPos = num

        return True
