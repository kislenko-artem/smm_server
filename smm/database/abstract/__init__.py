from abc import ABC
from typing import Iterable, List, Any


class Methods(ABC):

    async def init(self, *args, **kwargs):
        raise NotImplemented("")

    async def close(self):
        raise NotImplemented("")

    async def select(self, query: str, columns: List[str],
                     parameters: Iterable[Any] = None) -> List[dict]:
        raise NotImplemented("")

    async def execute(self, query: str, parameters: Iterable[Any] = None):
        raise NotImplemented("")

    async def insert(self, query: str, parameters: Iterable[Any] = None) -> int:
        raise NotImplemented("")
