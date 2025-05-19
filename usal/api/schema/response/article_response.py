from datetime import datetime
from usal.api.schema.response.author_response import (
    GetAuthorResponse,
    ViewAuthorDetailsResponse,
)
from usal.core import BaseSchema, PaginatedSchema


class ViewArticleDetailsResponse(BaseSchema):
    """
    Response to get an article.
    """

    id: str
    created_at: datetime
    title: str
    cover_image: str
    duration: str | None
    media: list[str] | None
    content: str
    author: ViewAuthorDetailsResponse
    category: str


class GetArticleResponse(BaseSchema):
    """
    Response to get an article.
    """

    id: str
    title: str
    cover_image: str
    author: GetAuthorResponse


class ListArticlesResponse(PaginatedSchema):
    """
    Response to list articles.
    """

    records: list[GetArticleResponse]


class ArticleCategoriesResponse(BaseSchema):
    """
    Response to list article categories.
    """

    id: str
    name: str


class ListArticleCategoriesResponse(BaseSchema):
    """
    Response to list article categories.
    """

    records: list[ArticleCategoriesResponse]
