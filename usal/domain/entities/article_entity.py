from datetime import datetime
from uuid import UUID
from usal.core import BaseEntity
from usal.domain.entities.author_entity import GetAuthorEntity, ViewAuthorDetailsEntity
from usal.domain.entities.common_entity import PageEntity


class ArticleCategoriesEntity(BaseEntity):
    """
    Response to list article categories.
    """

    id: UUID
    name: str


class ListArticleCategoriesEntity(BaseEntity):
    """
    Response to list article categories.
    """

    records: list[ArticleCategoriesEntity]


class ViewArticleDetailsEntity(BaseEntity):
    """
    Response to view an article.
    """

    id: UUID
    created_at: datetime
    title: str
    cover_image: str
    duration: str | None
    media: list[str] | None
    content: str
    author: ViewAuthorDetailsEntity
    category: ArticleCategoriesEntity


class GetArticleEntity(BaseEntity):
    """
    Response to get an article.
    """

    id: UUID
    title: str
    cover_image: str
    author: GetAuthorEntity


class ListArticlesEntity(BaseEntity):
    """
    Response to list articles.
    """

    page_info: PageEntity
    records: list[GetArticleEntity]


class GetAdminArticleEntity(BaseEntity):
    """
    Response to get an article.
    """

    id: UUID
    title: str
    cover_image: str
    author: GetAuthorEntity
    status: str
    type: str


class ListAdminArticlesEntity(BaseEntity):
    """
    Response to list articles.
    """

    page_info: PageEntity
    records: list[GetAdminArticleEntity]
