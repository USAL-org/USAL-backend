from typing import override
from uuid import UUID
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.user_entity import GetUserEntity, VerifyUserEntity
from usal.domain.repositories.user_repo import UserRepo
from usal.infrastructure.queries.user import (
    create_user_async_edgeql,
    get_user_by_email_async_edgeql,
    get_user_by_id_async_edgeql,
    update_password_async_edgeql,
    user_exists_async_edgeql,
    verify_user_async_edgeql,
)


class DbUserRepo(UserRepo):
    @override
    async def user_create(
        self,
        full_name: str,
        email: str,
        phone_number: str,
        password: str,
    ) -> VerifyUserEntity:
        async with self.session() as session:
            db_create_user = await create_user_async_edgeql.create_user(
                session,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            if not db_create_user:
                raise api_exception(
                    message="Unable to create user. Please try again.",
                )
            return VerifyUserEntity.model_validate(db_create_user, from_attributes=True)

    @override
    async def user_exists(self, email: str) -> bool:
        async with self.session() as session:
            return await user_exists_async_edgeql.user_exists(
                session,
                email=email,
            )

    @override
    async def get_by_email(self, email: str) -> VerifyUserEntity:
        async with self.session() as session:
            db_user = await get_user_by_email_async_edgeql.get_user_by_email(
                session,
                email=email,
            )
            if not db_user:
                raise api_exception(
                    message="User not found.",
                )
            return VerifyUserEntity.model_validate(db_user, from_attributes=True)

    @override
    async def verify_user(self, user_id: UUID) -> None:
        async with self.session() as session:
            db_user_verify = await verify_user_async_edgeql.verify_user(
                session,
                user_id=user_id,
            )
            if not db_user_verify:
                raise api_exception(
                    message="Unable to verify user.",
                )

    @override
    async def update_password(self, user_id: UUID, new_password: str) -> None:
        async with self.session() as session:
            db_update_password = await update_password_async_edgeql.update_password(
                session,
                user_id=user_id,
                new_password=new_password,
            )
            if not db_update_password:
                raise api_exception(
                    message="Unable to update user password.",
                )

    @override
    async def get_user_by_id(self, user_id: UUID) -> GetUserEntity:
        async with self.session() as session:
            db_user = await get_user_by_id_async_edgeql.get_user_by_id(
                session,
                user_id=user_id,
            )
            if not db_user:
                raise api_exception(
                    message="User not found.",
                )
            return GetUserEntity.model_validate(db_user, from_attributes=True)
