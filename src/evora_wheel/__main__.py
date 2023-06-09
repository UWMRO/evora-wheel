#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-05-05
# @Filename: __main__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
import functools
import os

import click
from click_default_group import DefaultGroup
from sdsstools.daemonizer import DaemonGroup

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
@click.option("--dummy", is_flag=True, help="Run the dummy wheel.")
@click.pass_context
def evora_wheel(ctx, dummy: bool = False):
    """Evora wheel actor."""

    ctx.obj = {"dummy": dummy}


@evora_wheel.group(cls=DaemonGroup, prog="evora_wheel", workdir=os.getcwd())
@click.pass_context
@cli_coro
async def actor(ctx):
    """Runs the actor."""

    dummy = ctx.obj.get("dummy", False)
    server = EvoraWheelServer(dummy=dummy)
    await server.start()


def main():
    evora_wheel()


if __name__ == "__main__":
    main()
