"""DICT client."""

import asyncio
from wordly.status_codes import Status
from wordly.parser import DictParser


class DictClient:
    def __init__(self, hostname: str = "dict.org", port: int = 2628) -> None:
        self.hostname = hostname
        self.port = port
        self.line_reader = DictParser()
        self.parsers = [self.line_reader]
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.READ_BYTES = 1024

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.hostname=}, {self.port=})"

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def connect(self):
        """
        Upon successful connection a status code of 220 is expected.
        """
        self.reader, self.writer = await asyncio.open_connection(
            self.hostname, self.port
        )
        connection_info = await self.reader.read(self.READ_BYTES)
        self.line_reader.feed(connection_info)

        if Status.INITIAL_CONNECTION.name in self.line_reader.mapping:
            return self.reader, self.writer

        raise ConnectionError(f"Could not connect to: {self.hostname=}, {self.port=}")

    async def disconnect(self):
        assert self.writer and self.reader
        self.writer.write(b"QUIT\r\n")
        await self.writer.drain()
        while Status.CLOSING_CONNECTION.name not in self.line_reader.mapping:
            closing_data = await self.reader.read(self.READ_BYTES)
            for line_reader in self.parsers:
                line_reader.feed(closing_data)
        self.writer.close()
        await self.writer.wait_closed()

    async def _send(self, command: bytes):
        if None in (self.reader, self.writer):
            self.reader, self.writer = await self.connect()
        else:
            new_line_reader = DictParser()
            new_line_reader.mapping[
                Status.INITIAL_CONNECTION.name
            ] = self.line_reader.mapping[Status.INITIAL_CONNECTION.name]
            self.line_reader = new_line_reader
            self.parsers.append(self.line_reader)

        assert self.reader and self.writer

        self.writer.write(command)
        await self.writer.drain()

        while (
            Status.COMMAND_COMPLETE.name not in self.line_reader.mapping
            and Status.NO_MATCH.name not in self.line_reader.mapping
        ):
            command_data = await self.reader.read(self.READ_BYTES)
            self.line_reader.feed(command_data)
        return self.line_reader

    async def define(self, word: str, database: str = "!") -> DictParser:
        command = f"DEFINE {database} {word}\r\n".encode()
        return await self._send(command)

    async def help(self) -> DictParser:
        command = "HELP\r\n".encode()
        return await self._send(command)

    async def match(self, word: str, database: str = "*", strategy: str = "."):
        """
        Match a word in a database using a strategy.
        """
        command = f"MATCH {database} {strategy} {word}".encode()
        return await self._send(command)

    async def show(self, option: str = "DB"):
        """
        Show more information
        """
        command = f"SHOW {option}".encode()
        return await self._send(command)
