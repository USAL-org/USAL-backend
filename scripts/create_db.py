import asyncio

import gel

from usal.core.config import DatabaseConfig
from usal.util.config import load_config

CONFIGURE_SYSTEM_QUERY = """
    CONFIGURE SYSTEM SET allow_user_specified_id := true;
"""


async def execute_query(
    client: gel.AsyncIOClient, query: str, params: dict = None
) -> None:
    try:
        await client.query(query, **(params or {}))
    except Exception:
        raise


async def configure_system(client: gel.AsyncIOClient) -> None:
    await execute_query(client, CONFIGURE_SYSTEM_QUERY)


async def main() -> None:
    load_config()
    config = DatabaseConfig.build()
    dsn = f"gel://{config.user}:{config.password}@{config.host}:{config.port}/{config.branch}"
    client = gel.create_async_client(dsn=dsn, tls_ca_file=config.tls_file)

    try:
        await configure_system(client)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
