# AUTOGENERATED FROM 'usal/infrastructure/queries/admin/check_superadmin_status.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import gel
import uuid


async def check_superadmin_status(
    executor: gel.AsyncIOExecutor,
    *,
    admin_id: uuid.UUID,
) -> bool:
    return await executor.query_single(
        """\
        SELECT EXISTS (
            SELECT Admin
            FILTER .id = <uuid>$admin_id
            AND .super_admin
        )\
        """,
        admin_id=admin_id,
    )
