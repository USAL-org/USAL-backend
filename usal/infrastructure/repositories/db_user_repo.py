from typing import override
from uuid import UUID
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.user_entity import VerifyUserEntity
from usal.domain.repositories.user_repo import UserRepo
from usal.infrastructure.queries.user import (
    create_user_async_edgeql,
    get_user_by_email_async_edgeql,
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
            article_obj = await create_user_async_edgeql.create_user(
                session,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            if not article_obj:
                raise api_exception(
                    message="Unable to create user. Please try again.",
                )
            return VerifyUserEntity.model_validate(article_obj, from_attributes=True)

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
            user = await get_user_by_email_async_edgeql.get_user_by_email(
                session,
                email=email,
            )
            if not user:
                raise api_exception(
                    message="User not found.",
                )
            return VerifyUserEntity.model_validate(user, from_attributes=True)

    @override
    async def verify_user(self, user_id: UUID) -> None:
        async with self.session() as session:
            user = await verify_user_async_edgeql.verify_user(
                session,
                user_id=user_id,
            )
            if not user:
                raise api_exception(
                    message="User not found.",
                )
