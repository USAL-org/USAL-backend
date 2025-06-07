from pydantic import Field, SecretStr
from usal.core import BaseRequest


class AdminLoginRequest(BaseRequest):
    username: str = Field(..., description="Admin's username (required).")
    password: SecretStr = Field(description="Admin's password (required).")
