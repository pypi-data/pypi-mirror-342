"""Wordly Utility classes."""

import asyncio
from collections import UserString
from wordly.client import DictClient
from wordly.status_codes import Status


class Word(UserString):
    def __init__(self, seq, hostname: str = "dict.org", port: int = 2628, client=None):
        super().__init__(seq)

        self.client = client or DictClient(hostname=hostname, port=port)
        self._cache = {}

    @property
    async def adefinition(self):
        if not self._cache:
            data = await self.client.define(self.data)
            self._cache.update(data.mapping)
        if definition := self._cache.get(Status.DEFINITION.name):
            return definition.decode()

    @property
    def definition(self):
        if not self._cache:
            loop = asyncio.get_event_loop()
            data = loop.run_until_complete(self.client.define(self.data))
            self._cache.update(data.mapping)
        if definition := self._cache.get(Status.DEFINITION.name):
            return definition.decode()
