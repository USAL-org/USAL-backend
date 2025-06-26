from datetime import datetime
from uuid import UUID
from usal.api.schema.response.author_response import (
    GetAuthorResponse,
    ViewAuthorDetailsResponse,
)
from usal.core import BaseSchema, PaginatedSchema
from usal.core.enums.article import ArticleStatus, ArticleType


class ArticleCategoriesResponse(BaseSchema):
    """
    Response to list article categories.
    """

    id: UUID
    name: str


class ListArticleCategoriesResponse(BaseSchema):
    """
    Response to list article categories.
    """

    records: list[ArticleCategoriesResponse]


class ViewArticleDetailsResponse(BaseSchema):
    """
    Response to get an article.
    """

    id: UUID
    created_at: datetime
    title: str
    cover_image: str
    duration: str | None
    media: list[str] | None
    content: str
    author: ViewAuthorDetailsResponse
    category: ArticleCategoriesResponse


class GetArticleResponse(BaseSchema):
    """
    Response to get an article.
    """

    id: UUID
    title: str
    cover_image: str
    created_at: datetime
    duration: str | None
    author: GetAuthorResponse


class ListArticlesResponse(PaginatedSchema):
    """
    Response to list articles.
    """

    records: list[GetArticleResponse]


class GetAdminArticleResponse(BaseSchema):
    """
    Response to get an article.
    """

    id: UUID
    title: str
    cover_image: str
    author: GetAuthorResponse
    status: ArticleStatus
    type: ArticleType


class ListAdminArticlesResponse(PaginatedSchema):
    """
    Response to list articles.
    """

    records: list[GetAdminArticleResponse]
