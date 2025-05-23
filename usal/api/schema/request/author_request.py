from pydantic import EmailStr, Field

from usal.api.schema.request.common_request import PaginationRequest
from usal.core import BaseRequest


class CreateAuthorRequest(BaseRequest):
    """
    Request to create an author.
    """

    full_name: str = Field(description="Name of an author.")
    email: EmailStr = Field(description="Email of the author.")
    pp_url: str | None = Field(None, description="Profile picture URL of the author.")
    short_description: str = Field(description="Short description of the author.")
    description: str | None = Field(None, description="Description of the author.")
    social_links: list[str] | None = Field(
        None, description="List of social links of the author."
    )


class UpdateAuthorRequest(BaseRequest):
    """
    Request to update an author.
    """

    full_name: str | None = Field(None, description="Name of an author.")
    email: EmailStr | None = Field(None, description="Email of the author.")
    pp_url: str | None = Field(None, description="Profile picture URL of the author.")
    short_description: str | None = Field(
        None, description="Short description of the author."
    )
    description: str | None = Field(None, description="Description of the author.")
    social_links: list[str] | None = Field(
        None, description="List of social links of the author."
    )


class FilterAuthorRequest(PaginationRequest):
    """
    Request to filter authors.
    """

    search: str | None = Field(None, description="Name of an author.")
