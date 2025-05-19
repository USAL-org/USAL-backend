from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps
from typing import Any, Callable, TypeAlias
from uuid import UUID

from fastapi import status

UserIdType: TypeAlias = UUID | str | int
PayloadType: TypeAlias = Any | None
DecoratedCallable: TypeAlias = Callable[..., Any]


class AuthorizationError(Exception):
    """Base exception for authorization errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ) -> None:
        """
        Initialize the AuthorizationError with a message and an optional status code.

        Args:
            message: The error message.
            status_code: The HTTP status code (default is 403 Forbidden).
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class PermissionDelegate(ABC):
    """Abstract base class for getting user permissions."""

    @abstractmethod
    async def validate_user(self, user_id: UserIdType) -> bool:
        """
        Validate if the user with the given user_id exists and is authorized.

        Args:
            user_id: User identifier to validate

        Returns:
            True if the user is valid, False otherwise
        """
        pass


def extract_user_id(payload: PayloadType, kwargs: dict) -> UserIdType:
    """
    Extract the user ID from the payload or kwargs (typically from the request).

    Args:
        payload: Request payload which may contain user identification attributes.
        kwargs: Additional arguments which may contain user identification information.

    Returns:
        The extracted user ID.

    Raises:
        AuthorizationError: If no user ID is found in the request (either payload or kwargs).
    """
    if payload:
        for attr in ("admin_id", "user_id", "id"):
            user_id = getattr(payload, attr, None)
            if user_id is not None:
                return user_id

    for key in ("user_id", "admin_id"):
        if key in kwargs:
            return kwargs[key]

    raise AuthorizationError(
        message="No user ID found in request", status_code=status.HTTP_400_BAD_REQUEST
    )


def require_permissions[T: Enum](
    delegate: PermissionDelegate,
) -> DecoratedCallable:
    """
    Decorator factory for permission-based access control.

    This decorator checks if the user has the required permissions before executing the decorated function.

    Args:
        required_permissions: List of (resource, CRUD permissions) pairs required for access.
        delegate: An instance of PermissionDelegate to fetch and validate the user's permissions.

    Returns:
        A decorator function that adds permission checks to the decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, payload: PayloadType, **kwargs: Any) -> Any:  # noqa: ANN401
            user_id = extract_user_id(payload, kwargs)

            if not await delegate.validate_user(user_id):
                raise AuthorizationError(
                    message="Unauthorized user", status_code=status.HTTP_403_FORBIDDEN
                )

            return await func(*args, payload=payload, **kwargs)

        return wrapper

    return decorator
