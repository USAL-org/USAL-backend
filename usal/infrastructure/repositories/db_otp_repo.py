from asyncio import create_task
from datetime import datetime, timezone
from typing import override
from uuid import UUID

from fastapi import status

from usal.core.database import Database
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.user_entity import OTPEntity
from usal.domain.repositories.otp_repo import OTPRepo
from usal.domain.repositories.sender_repo import SenderRepo
from usal.infrastructure.queries.otp import (
    create_otp_async_edgeql,
    get_otp_by_id_async_edgeql,
)
from usal.util.otp import calculate_expiration_time, generate_random_digits
from usal.util.password_crypt import get_hashed_password, verify_password


class DbOTPRepo(OTPRepo):
    def __init__(self, repo: SenderRepo, db: Database) -> None:
        super().__init__(db)
        self.repo = repo

    @override
    async def generate_otp(
        self,
        secret: str,
        expiration_time: datetime,
        user_id: UUID,
    ) -> OTPEntity:
        async with self.session() as session:
            db_otp = await create_otp_async_edgeql.create_otp(
                session,
                user_id=user_id,
                secret=secret,
                expiration_time=expiration_time,
            )
            if not db_otp:
                raise api_exception(
                    "Unable to create OTP. Please try again.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return OTPEntity.model_validate(db_otp, from_attributes=True)

    @override
    async def get_otp(self, verification_id: UUID) -> OTPEntity:
        async with self.session() as session:
            db_otp = await get_otp_by_id_async_edgeql.get_otp_by_id(
                session,
                verification_id=verification_id,
            )
            if not db_otp:
                raise Exception("OTP not found.")

            return OTPEntity.model_validate(db_otp, from_attributes=True)

    @override
    async def save_and_send(
        self,
        name: str,
        user_id: UUID,
        email: str | None = None,
        resend: bool | None = False,
    ) -> OTPEntity:
        expiration_time = 60 * 24
        secret = generate_random_digits()
        otp = await self.generate_otp(
            user_id=user_id,
            secret=get_hashed_password(secret),
            expiration_time=calculate_expiration_time(expiration_time),
        )
        if not otp:
            raise Exception("OTP not found.")
        if resend:
            create_task(self.repo.resend_link(otp.id, secret, name, email))
            return otp
        create_task(self.repo.send_otp(message_to=email, otp=secret, name=name))
        return otp

    @override
    async def verify(
        self,
        verification_id: UUID,
        secret: str,
    ) -> OTPEntity:
        otp = await self.get_otp(verification_id)

        if not otp:
            raise api_exception(
                "The verification id is invalid.",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        if otp.expiration_time <= datetime.now(timezone.utc) or not verify_password(
            secret, otp.secret
        ):
            raise api_exception(
                "Invalid OTP.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return otp
