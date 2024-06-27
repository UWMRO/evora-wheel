#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-05-05
# @Filename: __main__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
import functools

import click
from click_default_group import DefaultGroup
from daemonocle import DaemonCLI

from evora_wheel.server import EvoraWheelServer


def cli_coro(f):
    """Decorator function that allows defining coroutines with click."""

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return functools.update_wrapper(wrapper, f)


@click.group(
    name="evora-wheel",
    cls=DefaultGroup,
    default="actor",
    default_if_no_args=True,
)
def evora_wheel():
    """Evora wheel actor."""

    pass


@evora_wheel.group(
    cls=DaemonCLI,
    daemon_params={"pid_file": "/tmp/evora_wheel.pid"},
)
@click.option("--dummy", is_flag=True, help="Run the dummy wheel.")
@cli_coro
async def actor(dummy: bool = False):
    """Runs the actor."""

    server = EvoraWheelServer(dummy=dummy)
    await server.start()


def main():
    evora_wheel(obj={})


if __name__ == "__main__":
    main()
