from uuid import UUID
from usal.core import BaseEntity


class AuthorSocialLinkEntity(BaseEntity):
    """
    Author social link.
    """

    name: str
    url: str


class ViewAuthorDetailsEntity(BaseEntity):
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


class GetAuthorEntity(BaseEntity):
    """
    Response to get an author.
    """

    id: UUID
    full_name: str
    pp_url: str | None


class ListAuthorsEntity(BaseEntity):
    """
    Response to list authors.
    """

    records: list[GetAuthorEntity]
