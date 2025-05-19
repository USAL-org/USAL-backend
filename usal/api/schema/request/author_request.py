from pydantic import EmailStr, Field

from usal.core import BaseRequest


class CreateAuthorRequest(BaseRequest):
    """
    Request to create an author.
    """

    full_name: str = Field(description="Name of an author.")
    email: EmailStr = Field(description="Email of the author.")
    pp_url: str = Field(description="Profile picture URL of the author.")
    short_description: str = Field(description="Short description of the author.")
    description: str | None = Field(None, description="Description of the author.")
    social_links: list[str] = Field(description="List of social links of the author.")
