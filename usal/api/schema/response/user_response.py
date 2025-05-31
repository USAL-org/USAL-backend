from uuid import UUID
from usal.core import BaseSchema


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
