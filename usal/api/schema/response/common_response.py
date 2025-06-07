from usal.core import BaseSchema


class MessageResponse(BaseSchema):
    message: str


class TokenResponse(BaseSchema):
    access_token: str
