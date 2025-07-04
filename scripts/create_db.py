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

INSERT_SHA_QUERY = """
insert DefaultSha {
    key := <str>$key,
    hash := <str>$hash
};
"""

UPDATE_SHA_QUERY = """
update DefaultSha
filter .key = <str>$key
set {
    hash := <str>$hash
};
"""


INSERT_DEGREE_QUERY = """
with
    existing_actions := (
        select Degree {
            name
        }
    ),
    degrees_to_insert := (
        array_unpack(<array<DegreeNames>>[
            'ASSOCIATES_DEGREE', 
            'BACHELORS_DEGREE', 
            'MASTERS_DEGREE', 
            'DOCTORAL_DEGREE',])
        except existing_actions.name
    )
for degree_name in degrees_to_insert
union (
    insert Degree {
        name := degree_name
    }
);
"""

VERIFY_DEGREE_QUERY = """
select Degree {
    name
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
        print(f"Admin with username '{username}' already exists.")
        return

    params = {
        "username": username,
        "password_hash": password,
        "email": email,
        "super_admin": super_admin,
    }
    await execute_query(client, CREATE_ADMIN_QUERY, params)
    print(f"Admin with username '{username}' created successfully.")


async def add_degrees(client: gel.AsyncIOClient) -> None:
    await client.query(INSERT_DEGREE_QUERY)

    degrees = await client.query(VERIFY_DEGREE_QUERY)
    for degree in degrees:
        print(f"- {degree.name}")


async def populate_default_data(
    client: gel.AsyncIOClient,
    file_path: str,
    type_name: str,
    mapping: dict[str, str] | None = None,
    sheet_name: str | None = None,
) -> None:
    try:
        # print(f"Deleting existing {type_name} data...")
        # await execute_query(client, f"delete {type_name};")

        print(f"Converting Excel data from {file_path}...")
        data = await convert_excel_data_into_dictionary(
            client, file_path, mapping, sheet_name
        )
        print(f"Parsed {len(data)} rows from {file_path}")
        print("First 2 rows of parsed data:", data[:2])

        if not data:
            print(f"No data found in {file_path}")
            return

        for i, row in enumerate(data):
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
            try:
                await client.query(query, **row)
            except Exception as e:
                print(f"Error inserting row {i + 1}: {str(e)}")
                print(f"Row data: {row}")
                raise

        print(f"Successfully inserted {len(data)} records for {type_name}")
    except Exception as e:
        print(f"Unexpected error processing {type_name}: {str(e)}")
        raise


async def validate_and_update_default_data(
    client: gel.AsyncIOClient, data_dir: str = "usal/defaults/data"
) -> None:
    print("Starting validation of default data SHA256 hashes...")

    for root, _, files in os.walk(data_dir):
        for filename in files:
            # Skip temporary Excel files
            if filename.startswith("~$") or filename.startswith("."):
                print(f"Skipping temporary/hidden file: {filename}")
                continue

            full_file_path = os.path.join(root, filename)

            # Check if this file is in our DEFAULT_DATA_DICT
            # Try different key formats that might be used
            possible_keys = [
                full_file_path,
                filename,
                os.path.relpath(full_file_path),
                full_file_path.replace(os.sep, "/"),
            ]

            file_config = None
            used_key = None
            for key in possible_keys:
                if key in DEFAULT_DATA_DICT:
                    file_config = DEFAULT_DATA_DICT[key]
                    used_key = key
                    break

            if not file_config:
                print(
                    f"File {full_file_path} not found in DEFAULT_DATA_DICT, skipping..."
                )
                continue

            print(f"Processing file: {full_file_path}")
            print(f"Calculating SHA256 hash for file: {full_file_path}")
            current_hash = await calculate_file_hash(full_file_path)
            print(f"SHA256 hash: {current_hash}")

            # Check if hash exists in database
            existing_hash = await client.query_single(
                """
                select DefaultSha {
                    hash
                } filter .key = <str>$key
                limit 1;
                """,
                key=used_key,
            )

            should_populate = False

            if existing_hash:
                print(f"Found existing hash for {used_key}")
                if current_hash != existing_hash.hash:
                    print(f"Hash changed for {used_key}, updating data...")
                    await execute_query(
                        client,
                        UPDATE_SHA_QUERY,
                        params={"key": used_key, "hash": current_hash},
                    )
                    should_populate = True
                else:
                    print(f"Hash unchanged for {used_key}, skipping data population")
            else:
                print(f"No existing hash found for {used_key}, creating new entry...")
                await execute_query(
                    client,
                    INSERT_SHA_QUERY,
                    params={"key": used_key, "hash": current_hash},
                )
                should_populate = True

            if should_populate:
                print(f"Populating data for {used_key}...")
                for edgedb_type, input_model, sheet_name in file_config:
                    print(f"  Processing {edgedb_type} from sheet '{sheet_name}'")
                    await populate_default_data(
                        client,
                        full_file_path,
                        edgedb_type,
                        mapping=get_field_mapping(input_model),
                        sheet_name=sheet_name,
                    )
                print(f"Completed populating data for {used_key}")
            else:
                print(f"Skipped populating data for {used_key} (no changes)")

    print("Default data validation and updates completed.")


async def main() -> None:
    load_config()
    config = DatabaseConfig.build()
    dsn = f"gel://{config.user}:{config.password}@{config.host}:{config.port}/{config.branch}"
    client = gel.create_async_client(dsn=dsn, tls_ca_file=config.tls_file)

    try:
        await configure_system(client)
        await create_super_admin(client)
        await add_degrees(client)
        await validate_and_update_default_data(client)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
