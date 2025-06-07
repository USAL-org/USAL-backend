from typing import Callable, cast
from uuid import UUID

from fastapi import status
from gel import AsyncIOClient

from usal.core.container import container
from usal.core.database import Database
from usal.core.exceptions.api_exception import api_exception
from usal.core.permission_checker import (
    Permission,
    PermissionDelegate,
    UserIdType,
    require_permissions,
    AdminPermissions,
)
from usal.infrastructure.queries.admin import (
    check_admin_exists_async_edgeql,
    check_superadmin_status_async_edgeql,
    get_admin_permissions_async_edgeql,
)


async def get_admin_permissions(
    session: AsyncIOClient, admin_id: UserIdType
) -> list[Permission]:
    try:
        results = await get_admin_permissions_async_edgeql.get_admin_permissions(
            executor=session, admin_id=cast(UUID, admin_id)
        )

        if not results:
            print(f"No permissions found for admin {admin_id}")
            return []

        permissions = []
        for result in results:
            for perm in result.permission:
                permissions.append(Permission(AdminPermissions(perm.value)))
                print(f"Added permission: {perm.value}")

        return permissions

    except Exception as e:
        print(f"Error fetching permissions: {str(e)}")
        raise api_exception(
            "Failed to fetch permissions",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def user_exists(admin_id: UserIdType) -> bool:
    async with container.get(Database).session() as session:
        return await check_admin_exists_async_edgeql.check_admin_exists(
            executor=session, admin_id=cast(UUID, admin_id)
        )


class DBPermissionDelegate(PermissionDelegate):
    async def get_permissions(self, user_id: UserIdType) -> list[Permission]:
        async with container.get(Database).session() as session:
            try:
                return await get_admin_permissions(session, user_id)
            except Exception as e:
                raise api_exception(
                    f"Error fetching permissions: {str(e)}",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    async def validate_user(self, user_id: UserIdType) -> bool:
        try:
            return await user_exists(user_id)
        except Exception as e:
            raise api_exception(
                f"Error validating user: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def is_superadmin(self, user_id: UserIdType) -> bool:
        async with container.get(Database).session() as session:
            try:
                return (
                    await check_superadmin_status_async_edgeql.check_superadmin_status(
                        executor=session,
                        admin_id=cast(UUID, user_id),
                    )
                )
            except Exception as e:
                raise api_exception(
                    f"Error checking superadmin status: {str(e)}",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


permission_delegate = DBPermissionDelegate()


def perms(
    *required_perms: AdminPermissions,
) -> Callable[[Callable], Callable]:
    """
    Decorator to check if the user has the required permissions for a given endpoint.

    Args:
        *required_perms: A variable number of AdminPermissions enum values that represent
                        the permissions required for the decorated function.

    Returns:
        A decorator that checks permissions before allowing access to the decorated function.

    Example usage:
    ```python
    @router.post("/articles")
    @perms(AdminPermissions.ARTICLE_MANAGEMENT)
    async def create_article(request: Request, payload: Payload):
        pass

    @perms(
        AdminPermissions.ARTICLE_MANAGEMENT,
        AdminPermissions.USER_MANAGEMENT,
    )
    async def manage_content(request: Request, payload: Payload):
        pass
    ```
    """
    return require_permissions(*required_perms, delegate=permission_delegate)
