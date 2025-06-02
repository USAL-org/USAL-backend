from datetime import datetime
from uuid import UUID
from usal.core import BaseEntity


class OTPSentEntity(BaseEntity):
    verification_id: UUID
    destination: str


class OTPReSentEntity(BaseEntity):
    verification_id: UUID


class OTPEntity(BaseEntity):
    id: UUID
    user_id: UUID | None
    secret: str
    expiration_time: datetime


class VerificationTokenEntity(BaseEntity):
    token: str


class VerifyUserEntity(BaseEntity):
    id: UUID
    full_name: str
    email: str
    password_hash: str
    verified: bool


class GetUserEntity(BaseEntity):
    id: UUID
    full_name: str
    email: str
    phone_number: str
    password_hash: str
    gender: str | None
    verified: bool
    pp_url: str | None
    date_of_birth: datetime | None
