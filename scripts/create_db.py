import asyncio
import os

import gel

from scripts.constants import DEFAULT_DATA_DICT, get_field_mapping
from usal.core.config import DatabaseConfig
from usal.util.calculate_file_hash import calculate_file_hash
from usal.util.config import load_config
from usal.util.excel_file import convert_excel_data_into_dictionary
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


async def populate_default_data(
    client: gel.AsyncIOClient,
    file_path: str,
    type_name: str,
    mapping: dict[str, str] | None = None,
    sheet_name: str | None = None,
) -> None:
    try:
        await execute_query(client, f"delete {type_name};")

        data = await convert_excel_data_into_dictionary(
            client, file_path, mapping, sheet_name
        )

        if not data:
            return

        chunk_size = 1000
        total_inserted = 0

        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            try:
                for row in chunk:
                    if mapping:
                        mapped_row = {}
                        for file_col, db_field in mapping.items():
                            if file_col in row:
                                mapped_row[db_field] = row[file_col]
                        row = mapped_row

                    fields = ", ".join([f"{k} := <str>${k}" for k in row.keys()])
                    query = f"""
                        insert {type_name} {{
                            {fields}
                        }};
                    """

                    await client.query(query, **row)

                total_inserted += len(chunk)

            except Exception as e:
                print(
                    f"Error inserting chunk {i // chunk_size + 1} for {type_name}: {e}"
                )
                raise

        if total_inserted != len(data):
            raise Exception(
                f"Mismatch in inserted records for {type_name}: inserted {total_inserted}, expected {len(data)}"
            )

    except Exception as e:
        print(f"Unexpected error processing {type_name}: {str(e)}")
        raise


async def validate_and_update_default_data(
    client: gel.AsyncIOClient, file_path: str = "himalaya/defaults/data"
) -> None:
    try:
        for root, _, files in os.walk(file_path):
            for filename in files:
                full_file_path = os.path.join(root, filename)

                try:
                    current_hash = await calculate_file_hash(full_file_path)
                    existing_hash = await client.query_single(
                        """
                        select DefaultSHA { hash }
                        filter .key = <str>$key
                        limit 1;
                        """,
                        key=full_file_path,
                    )

                    should_process = False
                    if existing_hash:
                        if existing_hash.hash != current_hash:
                            should_process = True
                        else:
                            print(f"No change in hash for {full_file_path}, skipping.")
                    else:
                        should_process = True

                    if should_process:
                        for file_path, mappings in DEFAULT_DATA_DICT.items():
                            for edgedb_type, input_model, sheet_name in mappings:
                                await populate_default_data(
                                    client,
                                    file_path,
                                    edgedb_type,
                                    mapping=get_field_mapping(input_model),
                                    sheet_name=sheet_name,
                                )

                        if existing_hash:
                            await execute_query(
                                client,
                                """
                                update DefaultSHA
                                filter .key = <str>$key
                                set {
                                    hash := <str>$hash
                                };
                                """,
                                {"key": full_file_path, "hash": current_hash},
                            )
                        else:
                            await execute_query(
                                client,
                                """
                                insert DefaultSHA {
                                    key := <str>$key,
                                    hash := <str>$hash
                                };
                                """,
                                {"key": full_file_path, "hash": current_hash},
                            )
                except Exception as e:
                    print(f"Error processing file {full_file_path}: {str(e)}")
                    raise
        print("Default data validation and updates completed.")
    except Exception as e:
        print(f"Error in default data validation: {str(e)}")
        raise


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
