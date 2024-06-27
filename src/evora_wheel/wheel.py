#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-05-05
# @Filename: wheel.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

# Code adapted from
# https://github.com/UWMRO/filter_wheel/blob/master/src/filter_wheel/filter_wheel.py

__all__ = ["EvoraFilterWheel"]


import serial
from Phidget22.Devices.Stepper import Stepper, StepperControlMode


class FilterWheelError(Exception):
    """Filter wheel error."""

    pass


class EvoraFilterWheel:
    """The Evora filter wheel controller."""

    def __init__(self):
        "Sets up internal variables and initializes the stepper and serial port."

        self._VELOCITY_LIMIT = 5000
        self._filterPos = None
        self._hallData = None

        self.stepper = Stepper()
        self.stepper.openWaitForAttachment(10000)

        self.stepper.setControlMode(StepperControlMode.CONTROL_MODE_RUN)
        self.stepper.setAcceleration(20000)
        self.stepper.setCurrentLimit(0.9)

        self.SerialPortAddress = "/dev/ttyACM0"
        self.SerialPort = serial.Serial(self.SerialPortAddress, 9600, timeout=2)

    def disconnDev(self):
        "Disconnects the stepper and serial port."

        self.stepper.setVelocityLimit(0)
        self.stepper.setEngaged(False)
        self.stepper.close()
        self.SerialPort.close()

        return True

    def getHallData(self, index):
        """Gets the Hall sensor data and returns the sensor value at the index.

        Indices 0 and 1 store if a magnet is detected (0 returned) or not (1).

        """

        self.SerialPort.write(b"s")
        self._hallData = self.SerialPort.readline().rstrip(b"\r\n").split(b",")

        return int(self._hallData[index].decode())

    def getFilterPos(self):
        "Returns the position of the filterwheel, an integer between 0 and 5."

        return self._filterPos

    def home(self):
        "Homes the filter wheel to position 0."

        self.stepper.setEngaged(True)
        self.stepper.setVelocityLimit(self._VELOCITY_LIMIT)

        while self.getHallData(0) != 0 or self.getHallData(1) != 0:
            pass

        self._filterPos = 0

        self.stepper.setVelocityLimit(0)
        self.stepper.setEngaged(False)

        return True

    def moveFilter(self, num):
        "Moves the filter to the specified position, an integer between 0 and 5."

        self.stepper.setEngaged(True)
        self.stepper.setVelocityLimit(self._VELOCITY_LIMIT)

        if self._filterPos is None:
            self.home()

        assert isinstance(self._filterPos, int)

        if num >= self._filterPos:
            swaps = abs(num - self._filterPos)
        else:
            swaps = 6 - self._filterPos + num

        while swaps != 0:
            while self.getHallData(0) == 0:
                pass

            while self.getHallData(0) != 0:
                pass
            swaps -= 1

        self._filterPos = num

        self.stepper.setVelocityLimit(0)
        self.stepper.setEngaged(False)

        return True
