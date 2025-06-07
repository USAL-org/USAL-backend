from typing import Annotated

from fastapi import APIRouter, Depends
from wireup import Inject

from usal.api.schema.request.user_request import (
    ChangeForgottenPasswordRequest,
    ChangePasswordRequest,
    ForgetPasswordRequest,
    OTPRequest,
    ResendOtpRequest,
    UserLoginRequest,
    UserSignUpRequest,
)
from usal.api.schema.response.common_response import MessageResponse, TokenResponse
from usal.api.schema.response.user_response import (
    GetUserSchema,
    OTPSentResponse,
    OTPVerificationTokenResponse,
    ResendOTPSentResponse,
)
from usal.controllers.user_controller import UserController
from usal.core.api_response import APIResponse
from usal.core.jwt.jwt_bearer import JWTBearer
from usal.core.jwt.jwt_payload import JWTPayload

UserAuthRouter = APIRouter(
    tags=["User Auth"],
    prefix="/user-auth",
)


@UserAuthRouter.post("/sign-up")
async def user_sign_up(
    controller: Annotated[UserController, Inject()],
    request: UserSignUpRequest,
) -> APIResponse[OTPSentResponse]:
    return await controller.user_sign_up(request)


@UserAuthRouter.post("/verify")
async def verify_user(
    request: OTPRequest,
    controller: Annotated[UserController, Inject()],
) -> APIResponse[OTPVerificationTokenResponse]:
    return await controller.verify_otp(request)


@UserAuthRouter.post("/login")
async def user_login(
    controller: Annotated[UserController, Inject()],
    request: UserLoginRequest,
) -> APIResponse[TokenResponse | OTPSentResponse]:
    return await controller.user_login(request)


@UserAuthRouter.post("/forget-password")
async def forget_password(
    request: ForgetPasswordRequest,
    controller: Annotated[UserController, Inject()],
) -> APIResponse[OTPSentResponse]:
    return await controller.forget_password(request)


@UserAuthRouter.post("/change-forgotten-password")
async def change_forgotten_password(
    request: ChangeForgottenPasswordRequest,
    controller: Annotated[UserController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.change_forgotten_password(request)


@UserAuthRouter.post("/resend-otp")
async def resend_otp(
    input: ResendOtpRequest, controller: Annotated[UserController, Inject()]
) -> APIResponse[ResendOTPSentResponse]:
    return await controller.resend_otp(input.verification_id)


@UserAuthRouter.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    controller: Annotated[UserController, Inject()],
    payload: JWTPayload = Depends(JWTBearer("user")),
) -> APIResponse[MessageResponse]:
    return await controller.change_password(payload, request)


@UserAuthRouter.get("/logout")
async def user_logout(
    controller: Annotated[UserController, Inject()],
    payload: JWTPayload = Depends(JWTBearer("user")),
) -> APIResponse[MessageResponse]:
    return await controller.user_logout(payload)


@UserAuthRouter.get("/me")
async def get_user_info(
    controller: Annotated[UserController, Inject()],
    payload: JWTPayload = Depends(JWTBearer("user")),
) -> APIResponse[GetUserSchema]:
    return await controller.get_user_by_id(payload)
