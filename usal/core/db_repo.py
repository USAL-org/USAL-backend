from abc import ABCMeta
from contextlib import asynccontextmanager

from usal.core.database import AsyncSessionGenerator, Database


class DbRepo:
    def __init__(self, db: Database) -> None:
        self._db = db

    @asynccontextmanager
    async def session(self) -> AsyncSessionGenerator:
        async with self._db.session() as session:
            yield session


class Repo(metaclass=ABCMeta):
    __slots__ = ()
