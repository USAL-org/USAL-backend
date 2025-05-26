from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import UUID
import jwt
from fastapi import Request, status
from fastapi.security import HTTPBearer

from usal.core.exceptions.api_exception import api_exception
from usal.core.jwt.jwt_payload import JWTPayload

USER_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 15
ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"

USER_JWT_SECRET_KEY = "a7f8e2d4c9b6f1e8a3c7d2f9b4e6a1c8d5f2e9b7c4a6f3e1d8b5c2f7a4e9d6c3"
ADMIN_JWT_SECRET_KEY = (
    "f3e8d1c6b9a4f7e2d5c8b1a6f4e9d2c7b5a8f3e6d9c2b7a4f1e8d5c6b9a2f7e4"
)

USER_PREFIX = "dXNlcg==."
ADMIN_PREFIX = "YWRtaW4=."

TokenType = Literal["user", "admin"]


def create_token(
    subject_id: UUID, token_type: TokenType, expires_delta: int | None = None
) -> str:
    """Generic token creator for both users and admins"""
    if token_type == "user":
        prefix = USER_PREFIX
        secret = USER_JWT_SECRET_KEY
        default_expire = USER_ACCESS_TOKEN_EXPIRE_MINUTES
    else:
        prefix = ADMIN_PREFIX
        secret = ADMIN_JWT_SECRET_KEY
        default_expire = ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES

    expires_delta = expires_delta or default_expire
    expires = datetime.now(UTC) + timedelta(minutes=expires_delta)

    to_encode = {
        "exp": expires,
        "sub": str(subject_id),
        "type": token_type,
    }

    encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
    return prefix + encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, required_role: TokenType = "user", auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.required_role = required_role

    async def __call__(self, request: Request) -> JWTPayload:
        credentials = await super().__call__(request)

        if credentials is None:
            raise api_exception(
                "Missing authorization credentials", status.HTTP_401_UNAUTHORIZED
            )
        token = credentials.credentials

        payload = None
        token_type = None
        secret = None

        if token.startswith(USER_PREFIX):
            token = token[len(USER_PREFIX) :]
            secret = USER_JWT_SECRET_KEY
            token_type = "user"
        elif token.startswith(ADMIN_PREFIX):
            token = token[len(ADMIN_PREFIX) :]
            secret = ADMIN_JWT_SECRET_KEY
            token_type = "admin"
        else:
            raise api_exception("Unknown token prefix", status.HTTP_403_FORBIDDEN)

        try:
            payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise api_exception("Token has expired", status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            raise api_exception("Invalid token", status.HTTP_403_FORBIDDEN)

        if token_type != self.required_role:
            raise api_exception(
                f"{self.required_role.capitalize()} access required",
                status.HTTP_403_FORBIDDEN,
            )

        try:
            return JWTPayload(**payload)
        except Exception as e:
            raise api_exception(
                f"Invalid token payload: {str(e)}", status.HTTP_403_FORBIDDEN
            )
