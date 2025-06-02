from uuid import UUID
from usal.api.schema.request.user_request import (
    ChangeForgottenPasswordRequest,
    ChangePasswordRequest,
    ForgetPasswordRequest,
    OTPRequest,
    UserLoginRequest,
    UserSignUpRequest,
)
from usal.api.schema.response.common_response import (
    MessageResponse,
    TokenResponse,
)
from usal.api.schema.response.user_response import (
    GetUserSchema,
    OTPSentResponse,
    OTPVerificationTokenResponse,
    ResendOTPSentResponse,
)
from usal.core.api_response import APIResponse, api_response
from usal.core.exceptions.api_exception import api_exception
from usal.core.jwt.jwt_payload import JWTPayload
from usal.domain.entities.common_entity import TokenEntity
from usal.usecases.user_usecase import UserUsecase
from usal.util.password_crypt import decode_token


class UserController:
    def __init__(self, usecase: UserUsecase) -> None:
        self.usecase = usecase

    async def user_sign_up(
        self, request: UserSignUpRequest
    ) -> APIResponse[OTPSentResponse]:
        otp_response = await self.usecase.user_sign_up(request)
        if otp_response is None:
            raise api_exception(
                message="Failed to sign up user and send OTP.",
            )
        return api_response(
            OTPSentResponse.model_validate(otp_response, from_attributes=True)
        )

    async def user_login(
        self, request: UserLoginRequest
    ) -> APIResponse[TokenResponse | OTPSentResponse]:
        token_obj = await self.usecase.user_login(
            email=request.email,
            password=request.password,
        )

        return api_response(
            TokenResponse.model_validate(token_obj, from_attributes=True)
            if isinstance(token_obj, TokenEntity)
            else OTPSentResponse.model_validate(token_obj, from_attributes=True)
        )

    async def verify_otp(
        self, request: OTPRequest
    ) -> APIResponse[OTPVerificationTokenResponse]:
        result = await self.usecase.verify_otp(
            verification_id=request.verification_id, secret=request.otp
        )
        return api_response(
            OTPVerificationTokenResponse(
                message="OTP successfully verified.",
                token=result.token if result else None,
            )
        )

    async def forget_password(
        self, request: ForgetPasswordRequest
    ) -> APIResponse[OTPSentResponse]:
        opt_response = await self.usecase.forget_password(request.email)
        return api_response(
            OTPSentResponse.model_validate(opt_response, from_attributes=True)
        )

    async def change_forgotten_password(
        self, password_input: ChangeForgottenPasswordRequest
    ) -> APIResponse[MessageResponse]:
        try:
            payload = await decode_token(password_input.token)
            await self.usecase.change_forgotten_password(
                user_id=UUID(payload["sub"]), new_password=password_input.password
            )
            return api_response(MessageResponse(message="Password has been changed."))
        except Exception as e:
            raise api_exception(
                "Invalid or expired token. Please initiate the password reset process again."
            ) from e

    async def resend_otp(
        self, verification_id: UUID
    ) -> APIResponse[ResendOTPSentResponse]:
        otp_sent_entity = await self.usecase.resend_otp(verification_id)
        return api_response(
            ResendOTPSentResponse.model_validate(otp_sent_entity, from_attributes=True)
        )

    async def change_password(
        self, payload: JWTPayload, request: ChangePasswordRequest
    ) -> APIResponse[MessageResponse]:
        await self.usecase.change_password(payload, request)
        return api_response(MessageResponse(message="Password has been changed."))

    async def user_logout(self, payload: JWTPayload) -> APIResponse[MessageResponse]:
        try:
            await self.usecase.logout(payload)
            return api_response(
                MessageResponse(message="User successfully logged out.")
            )
        except Exception as e:
            raise api_exception(
                "Failed to log out. Please try again later.",
                status_code=500,
                exception=e,
            )

    async def get_user_by_id(self, payload: JWTPayload) -> APIResponse[GetUserSchema]:
        try:
            user = await self.usecase.get_user_by_id(payload)
            return api_response(
                GetUserSchema.model_validate(user, from_attributes=True)
            )
        except Exception as e:
            raise api_exception(
                "Failed to retrieve user information.",
                status_code=500,
                exception=e,
            )
