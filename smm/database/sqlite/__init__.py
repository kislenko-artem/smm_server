from os import path
from typing import Iterable, Any, List

import aiosqlite

from smm.config import BASE_DIR
from smm.database.sqlite.profiles import Profiles
from smm.database.sqlite.vk_groups import Groups
from smm.database.sqlite.business import Business


class Methods(Profiles, Groups, Business):
    __slots__ = ("path",)

    async def init(self, *args, **kwargs):
        to_migrate_script = path.join(BASE_DIR, 'database', 'sqlite', 'migrations.sql')
        self.path = path.join(BASE_DIR, 'sqlite_python.db')
        async with aiosqlite.connect(self.path) as db:
            with open(to_migrate_script) as f:
                for statement in f.read().split("--split"):
                    await db.execute(statement)
            await db.commit()

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

    async def insert(self, query: str, parameters: Iterable[Any] = None) -> int:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(query, parameters) as cursor:
                await db.execute(query, parameters)
                id = cursor.lastrowid
            await db.commit()
        return id
