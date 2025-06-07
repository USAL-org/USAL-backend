from datetime import datetime, timedelta, timezone
from uuid import UUID
from passlib.context import CryptContext

import jwt
from typing import Any

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USER_JWT_SECRET_KEY = "a7f8e2d4c9b6f1e8a3c7d2f9b4e6a1c8d5f2e9b7c4a6f3e1d8b5c2f7a4e9d6c3"
ALGORITHM = "HS256"


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def create_reset_token(user_id: UUID, expires_in: int = 3600) -> str:
    exp = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    payload: dict[str, Any] = {"sub": str(user_id), "exp": exp}
    token: str = jwt.encode(payload, USER_JWT_SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    return token


async def decode_token(token: str) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(  # type: ignore
            token, USER_JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        raise ValueError(f"Token decode failed: {str(e)}")
