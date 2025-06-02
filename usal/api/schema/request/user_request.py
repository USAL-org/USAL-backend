from typing import Self
from uuid import UUID
from pydantic import EmailStr, Field, model_validator
from usal.core import BaseRequest


class UserSignUpRequest(BaseRequest):
    """Request schema for user sign-up."""

    full_name: str = Field(..., description="User's full name (required).")
    email: EmailStr = Field(..., description="User's email (required).")
    phone_number: str = Field(..., description="User's phone number (required).")
    password: str = Field(description="User's password (required).")
    confirm_password: str = Field(
        description="Confirmation of the user's password (required)."
    )

    @model_validator(mode="after")
    def validate_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Password and confirm password do not match.")
        return self


class UserLoginRequest(BaseRequest):
    """Request schema for user login."""

    email: EmailStr = Field(..., description="User's email (required).")
    password: str = Field(description="Admin's password (required).")


class OTPRequest(BaseRequest):
    """Request schema for OTP verification."""

    verification_id: UUID = Field(
        ..., description="The unique verification identifier."
    )
    otp: str = Field(..., description="The one-time password (OTP) sent to the user.")


class ChangePasswordRequest(BaseRequest):
    """Request schema for changing user password."""

    old_password: str = Field(..., description="User's old password.")
    new_password: str = Field(
        min_length=6,
        description=(
            "User's password must be at least 8 characters long and include: "
            "at least one uppercase letter, one lowercase letter, one digit, "
            "and one special character (!@#$%^&*()_-+={}[]|:;<>,.?/~)."
        ),
    )


class ResendOtpRequest(BaseRequest):
    """Request schema for resending OTP."""

    verification_id: UUID = Field(
        ..., description="The unique verification identifier."
    )


class ChangeForgottenPasswordRequest(BaseRequest):
    """Request schema for changing forgotten password."""

    password: str = Field(
        min_length=6,
        strict=True,
        description=(
            "User's password must be at least 8 characters long and include: "
            "at least one uppercase letter, one lowercase letter, one digit, "
            "and one special character (!@#$%^&*()_-+={}[]|:;<>,.?/~)."
        ),
    )
    token: str = Field(
        description="The token used to reset the password. It is usually sent to the user's email or phone.",
    )


class ForgetPasswordRequest(BaseRequest):
    """Request schema for forgetting password."""

    email: EmailStr = Field(
        ...,
        description="The email address associated with the user's account.",
    )
