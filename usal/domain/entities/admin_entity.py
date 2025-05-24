from uuid import UUID

from pydantic import EmailStr

from usal.core import BaseEntity


class AdminEntity(BaseEntity):
    id: UUID
    username: str
    email: EmailStr
    password: str
