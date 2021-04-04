from os import path
from typing import Iterable, Any, List

import aiosqlite

from smm.config import BASE_DIR
from smm.database.sqlite.profiles import Profiles


class Methods(Profiles):
    __slots__ = ("path",)

    async def init(self, *args, **kwargs):
        self.path = path.join(BASE_DIR, 'sqlite_python.db')
        async with aiosqlite.connect(self.path) as db:
            pass

    async def close(self):
        pass

    async def select(self, query: str, columns: List[str],
                     parameters: Iterable[Any] = None) -> List[dict]:
        data: List[dict] = []
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(query, parameters) as cursor:
                async for row in cursor:
                    data.append(dict(zip(columns, row)))
        return data

    async def execute(self, query: str, parameters: Iterable[Any] = None):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(query, parameters)
            await db.commit()