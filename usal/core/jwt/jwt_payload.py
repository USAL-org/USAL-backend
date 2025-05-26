from datetime import UTC, datetime
from typing import Any, Literal
from uuid import UUID
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import EmailStr, Field

from fastapi import Request


class JWTPayload(HTTPAuthorizationCredentials):
    token_type: Literal["user", "admin"] = Field(..., alias="type")
    sub: UUID
    exp: datetime
    email: EmailStr | None = None
    email_verified: bool = False
    name: str | None = None
    picture: str | None = None
    scheme: str = ""
    credentials: str = ""

    @property
    def name_or_empty(self) -> str:
        return self.name if self.name else ""

    @property
    def email_or_empty(self) -> str:
        return self.email if self.email else ""

    @property
    def user_id(self) -> UUID:
        return self.sub

    @property
    def is_admin(self) -> bool:
        return self.token_type == "admin"

    @property
    def is_expired(self) -> bool:
        return datetime.now(UTC) > self.exp


class AuthRequest(Request):
    def __init__(self, request: Request, auth_payload: dict[str, Any]) -> None:
        super().__init__(request.scope, request._receive, request._send)
        self._payload = JWTPayload(**auth_payload)
        request.state.payload = self._payload  # Using state instead of direct attribute

    @property
    def payload(self) -> JWTPayload:
        return self._payload
