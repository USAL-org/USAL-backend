import logging
from typing import Any, Dict, Optional

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class APIError:
    def __init__(
        self,
        message: str,
        code: int | None = None,
        tag: str | None = None,
        error_code: str | None = None,
    ) -> None:
        self.message = message
        self.code = code
        self.tag = tag
        self.error_code = error_code

    def to_dict(self) -> dict[str, Any]:
        dict: Dict[str, Any] = {"message": self.message}

        if self.code is not None:
            dict["code"] = self.code

        if self.tag is not None:
            dict["tag"] = self.tag

        if self.error_code is not None:
            dict["error_code"] = self.error_code

        return dict


class APIException(Exception):
    def __init__(
        self, message: str, status_code: int, errors: list[APIError] = []
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "errors": [error.to_dict() for error in self.errors],
        }


def api_exception(
    message: str,
    status_code: int = 400,
    error_code: int | None = None,
    error_message: str | None = None,
    tag: str = "",
    exception: Exception | None = None,
) -> APIException:
    if exception:
        logging.exception(exception)

    if error_message and tag:
        return APIException(
            message,
            status_code,
            [APIError(message=error_message, tag=tag, code=error_code)],
        )

    return APIException(message, status_code)


def general_api_exception(
    error_code: Optional[int] = None,
    error_message: Optional[str] = None,
    tag: Optional[str] = None,
    exception: Optional[Exception] = None,
) -> APIException:
    if exception:
        logging.exception(exception)

    if error_message and tag:
        return APIException(
            message="Something went wrong. Please try again later.",
            status_code=500,
            errors=[APIError(message=error_message, code=error_code, tag=tag)],
        )

    return APIException(
        message="Something went wrong. Please try again later.",
        status_code=500,
    )


async def custom_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Custom exception handler for Pydantic validation errors.

    :param request: The incoming request.
    :type request: Request
    :param exc: The validation exception.
    :type exc: RequestValidationError

    :return: JSONResponse with validation error details.
    :rtype: JSONResponse
    """
    error_details = []
    for error in exc.errors():
        loc = ".".join(map(str, error["loc"]))  # Convert all elements to strings
        msg = error["msg"]
        type_ = error["type"]
        error_details.append({"loc": loc, "msg": msg, "type": type_})

    response_data = {"detail": error_details}
    return JSONResponse(content=response_data, status_code=400)
