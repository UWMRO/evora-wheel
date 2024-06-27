#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-05-05
# @Filename: server.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from typing import Callable

from evora_wheel import EvoraFilterWheel, EvoraFilterWheelDummy
from evora_wheel.wheel import FilterWheelError


__all__ = ["EvoraWheelServer"]


PORT = 9999


class EvoraWheelServer:
    """TCP server for the filter wheel."""

    def __init__(self, dummy: bool = False):
        self.server: asyncio.Server | None = None

        if dummy:
            self.wheel = EvoraFilterWheelDummy()
        else:
            self.wheel = EvoraFilterWheel()

    async def start(self):
        """Starts the server and serve forever."""

        self.server = await asyncio.start_server(self.handle_message, "0.0.0.0", PORT)

        addrs = ", ".join(str(sock.getsockname()) for sock in self.server.sockets)

        try:
            async with self.server:
                await self.server.serve_forever()
        finally:
            self.server.close()

    async def handle_message(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ):
        """Handles messages received from the client."""

        data = await reader.readline()
        message = data.decode().strip()

        try:
            reply = ""
            if message.startswith("home"):
                await self.run(self.wheel.home)
            elif message.startswith("move"):
                num = int(message.split()[1])
                await self.run(self.wheel.moveFilter, num)
            elif message.startswith("get"):
                reply = str(await self.run(self.wheel.getFilterPos))
            else:
                raise FilterWheelError(f"Unknown command {message}")
        except Exception as err:
            writer.write((f"ERR,{err}\n").encode())
        else:
            writer.write(b"OK")
            if reply != "":
                writer.write((f",{reply}").encode())

        await writer.drain()

        writer.close()
        await writer.wait_closed()

    async def run(self, method: Callable, *args):
        """Runs a method in an executor."""

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, method, *args)
