from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable

from fastapi import status
from gel import AsyncIOClient, create_async_client
from gel.errors import ClientConnectionError

from usal.core.config import DatabaseConfig
from usal.core.container import container
from usal.core.exceptions.api_exception import api_exception

SessionFactory = Callable[[], AsyncIOClient]
AsyncSessionGenerator = AsyncGenerator[AsyncIOClient, None]


@container.register
class Database:
    def __init__(self) -> None:
        self.config = DatabaseConfig.build()
        dsn = (
            f"gel://{self.config.user}:{self.config.password}"
            f"@{self.config.host}:{self.config.port}/{self.config.branch}"
        )
        self.client = create_async_client(dsn=dsn, tls_ca_file=self.config.tls_file)

    @asynccontextmanager
    async def session(self) -> AsyncSessionGenerator:
        try:
            async with self.client as session:
                yield session

        except ClientConnectionError as e:
            raise api_exception(
                "Something went wrong",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                error_message=str(e),
            )

    async def close(self) -> None:
        await self.client.aclose()
