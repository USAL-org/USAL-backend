from uuid import UUID
from usal.core import BaseSchema


class AuthorSocialLink(BaseSchema):
    """
    Author social link.
    """

    name: str
    url: str


class ViewAuthorDetailsResponse(BaseSchema):
    """
    Response to view an author.
    """

    id: UUID
    full_name: str
    email: str
    pp_url: str | None
    short_description: str
    description: str | None
    social_links: list[str] | None


class GetAuthorResponse(BaseSchema):
    """
    Response to get an author.
    """

    id: UUID
    full_name: str
    pp_url: str | None


class ListAuthorsResponse(BaseSchema):
    """
    Response to list authors.
    """

    records: list[GetAuthorResponse]
