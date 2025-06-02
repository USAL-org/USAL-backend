from fastapi import status

from usal.core.exceptions.api_exception import api_exception
from usal.core.jwt.jwt_bearer import create_token
from usal.domain.entities.common_entity import (
    TokenEntity,
)
from usal.domain.repositories.admin_repo import AdminRepo
from usal.util.password_crypt import verify_password


class AdminUsecase:
    def __init__(
        self,
        repo: AdminRepo,
    ) -> None:
        self.repo = repo

    async def login(self, username: str, password: str) -> TokenEntity:
        admin = await self.repo.get_admin_by_username(username)

        if not admin:
            raise api_exception(
                "Invalid username. Please try again.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if not verify_password(password, admin.password):
            raise api_exception(
                "Invalid Password.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return TokenEntity(
            access_token=create_token(subject_id=admin.id, token_type="user"),
        )
