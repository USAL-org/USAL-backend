from datetime import UTC, datetime
from uuid import UUID

from fastapi import status
from usal.api.schema.request.user_request import (
    ChangePasswordRequest,
    UserSignUpRequest,
)
from usal.core.exceptions.api_exception import api_exception
from usal.core.jwt.jwt_bearer import create_token
from usal.core.jwt.jwt_payload import JWTPayload
from usal.core.token_blacklist import add_token_to_blacklist
from usal.domain.entities.common_entity import TokenEntity
from usal.domain.entities.user_entity import (
    GetUserEntity,
    OTPReSentEntity,
    OTPSentEntity,
    VerificationTokenEntity,
)
from usal.domain.repositories.otp_repo import OTPRepo
from usal.domain.repositories.user_repo import UserRepo
from usal.util.password_crypt import (
    create_reset_token,
    get_hashed_password,
    verify_password,
)


class UserUsecase:
    def __init__(
        self,
        repo: UserRepo,
        otp_repo: OTPRepo,
    ) -> None:
        self.repo = repo
        self.otp_repo = otp_repo

    async def user_sign_up(self, request: UserSignUpRequest) -> OTPSentEntity | None:
        if await self.repo.user_exists(request.email):
            raise api_exception(
                "User already exists with this email.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = await self.repo.user_create(
                full_name=request.full_name,
                email=request.email,
                phone_number="9876543210",
                password=get_hashed_password(request.password),
            )
            if user:
                otp = await self.otp_repo.save_and_send(
                    user_id=user.id,
                    name=user.full_name,
                    email=user.email,
                )
                return OTPSentEntity(verification_id=otp.id, destination=user.email)
        except Exception as e:
            raise api_exception(
                "Error while saving otp for the user. Try to login with the same credential to get new otp.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=e,
            )

    async def user_login(
        self, email: str, password: str
    ) -> TokenEntity | OTPSentEntity:
        user = await self.repo.get_by_email(email)
        if not user:
            raise api_exception(
                "User not found.", status_code=status.HTTP_404_NOT_FOUND
            )

        if not verify_password(password, user.password_hash):
            raise api_exception(
                "The password is incorrect.", status_code=status.HTTP_401_UNAUTHORIZED
            )

        if not user.verified:
            otp = await self.otp_repo.save_and_send(
                user_id=user.id,
                name=user.full_name,
                email=user.email,
            )
            return OTPSentEntity(verification_id=otp.id, destination=user.email)

        return TokenEntity(
            access_token=create_token(subject_id=user.id, token_type="user"),
        )

    async def verify_otp(
        self, verification_id: UUID, secret: str
    ) -> VerificationTokenEntity | None:
        try:
            otp = await self.otp_repo.verify(
                verification_id,
                secret,
            )
            await self.repo.verify_user(otp.user_id)
            token = await create_reset_token(user_id=otp.user_id)
            return VerificationTokenEntity(token=token)
        except Exception as e:
            raise api_exception(
                "The user verification has failed.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=e,
            )

    async def forget_password(self, email: str) -> OTPSentEntity:
        user = await self.repo.get_by_email(email)
        if not user:
            raise api_exception(
                f"User with phone({email}) not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        otp = await self.otp_repo.save_and_send(
            user_id=user.id,
            name=user.full_name,
            email=user.email,
        )

        return OTPSentEntity(verification_id=otp.id, destination=user.email)

    async def change_forgotten_password(self, user_id: UUID, new_password: str) -> None:
        try:
            await self.repo.update_password(
                user_id=user_id,
                new_password=get_hashed_password(new_password),
            )

        except Exception as e:
            raise api_exception(
                "Unable to change password.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=e,
            )

    async def change_password(
        self, payload: JWTPayload, request: ChangePasswordRequest
    ) -> None:
        user = await self.repo.get_user_by_id(payload.user_id)
        if not verify_password(request.old_password, user.password_hash):
            raise api_exception(
                message="The old password is incorrect.",
                tag="old_password",
            )

        await self.repo.update_password(
            user_id=user.id,
            new_password=get_hashed_password(request.new_password),
        )
        await self.logout(payload)

    async def resend_otp(self, verification_id: UUID) -> OTPReSentEntity:
        try:
            otp = await self.otp_repo.get_otp(verification_id)
            user = await self.repo.get_user_by_id(otp.user_id)

            new_otp = await self.otp_repo.save_and_send(
                name=user.full_name,
                user_id=otp.user_id,
                email=user.email,
            )
            return OTPReSentEntity(verification_id=new_otp.id)

        except Exception as e:
            raise api_exception(
                "Unable to resend otp.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=e,
            )

    async def logout(self, payload: JWTPayload) -> None:
        try:
            token = payload.credentials
            print(f"Logging out user with token: {token}\n\n\n\n{payload}")
            if not token:
                raise api_exception("Invalid token", status.HTTP_400_BAD_REQUEST)

            remaining = int((payload.exp - datetime.now(UTC)).total_seconds())
            if remaining > 0:
                add_token_to_blacklist(token, remaining)

            return None
        except Exception as e:
            raise api_exception(
                "Failed to log out. Please try again later.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=e,
            )

    async def get_user_by_id(self, payload: JWTPayload) -> GetUserEntity:
        try:
            user = await self.repo.get_user_by_id(payload.user_id)
            return GetUserEntity.model_validate(user, from_attributes=True)
        except Exception as e:
            raise api_exception(
                "Failed to retrieve user information.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=e,
            ) from e
