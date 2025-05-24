import asyncio

import gel

from usal.core.config import DatabaseConfig
from usal.util.config import load_config
from usal.util.password_crypt import get_hashed_password


CONFIGURE_SYSTEM_QUERY = """
    CONFIGURE SYSTEM SET allow_user_specified_id := true;
"""

ADMIN_EXISTS_QUERY = """
select Admin {
    username
} filter .username = <str>$username
limit 1;
"""

CREATE_ADMIN_QUERY = """
insert Admin {
    username := <str>$username,
    password_hash := <str>$password_hash,
    email := <str>$email,
    super_admin := <bool>$super_admin,
};
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


async def create_super_admin(client: gel.AsyncIOClient) -> None:
    username = "usal_admin"
    email = "usal@gmail.com"
    password = get_hashed_password("Usaladmin@2025")
    super_admin = True

    existing_admin = await client.query_single(ADMIN_EXISTS_QUERY, username=username)

    if existing_admin:
        return

    params = {
        "username": username,
        "password_hash": password,
        "email": email,
        "super_admin": super_admin,
    }
    await execute_query(client, CREATE_ADMIN_QUERY, params)
    print(f"Admin with username '{username}' created successfully.")


async def main() -> None:
    load_config()
    config = DatabaseConfig.build()
    dsn = f"gel://{config.user}:{config.password}@{config.host}:{config.port}/{config.branch}"
    client = gel.create_async_client(dsn=dsn, tls_ca_file=config.tls_file)

    try:
        await configure_system(client)
        await create_super_admin(client)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
