from pydantic import BaseModel

from usal.core import BaseSchema


class APIResponse[T: BaseSchema](BaseModel):
    status: str
    data: T


class APIDictResponse[T](BaseModel):
    status: str = "success"
    data: dict[str, T]


def api_response[T: BaseSchema](data: T, status: str = "success") -> APIResponse[T]:
    return APIResponse(data=data, status=status)
