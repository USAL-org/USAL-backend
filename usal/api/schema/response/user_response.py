from datetime import datetime
from uuid import UUID
from usal.core import BaseSchema
from usal.core.enums.user import Gender


class OTPSentResponse(BaseSchema):
    """Response schema for OTP sent."""

    verification_id: UUID
    destination: str


class ResendOTPSentResponse(BaseSchema):
    """Response schema for resending OTP."""

    verification_id: UUID


class OTPVerificationTokenResponse(BaseSchema):
    """Response schema for OTP verification with token."""

    message: str
    token: str | None


class GetUserSchema(BaseSchema):
    """Schema for user details."""

    id: UUID
    full_name: str
    email: str
    phone_number: str
    password_hash: str
    gender: Gender | None
    verified: bool
    pp_url: str | None
    date_of_birth: datetime | None
