from typing import override

from fastapi import status
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.admin_entity import AdminEntity
from usal.domain.repositories.admin_repo import AdminRepo
from usal.infrastructure.queries.admin import get_admin_by_username_async_edgeql


class DbAdminRepo(AdminRepo):
    @override
    async def get_admin_by_username(self, username: str) -> AdminEntity:
        async with self.session() as session:
            admin = await get_admin_by_username_async_edgeql.get_admin_by_username(
                executor=session,
                username=username,
            )
            if not admin:
                raise api_exception(
                    "No admin found with the provided username. Please check the username and try again.",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            return AdminEntity.model_validate(admin, from_attributes=True)
