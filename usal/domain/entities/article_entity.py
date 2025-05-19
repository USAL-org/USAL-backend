from datetime import datetime
from usal.core import BaseEntity
from usal.domain.entities.author_entity import GetAuthorEntity, ViewAuthorDetailsEntity


class ViewArticleDetailsEntity(BaseEntity):
    """
    Response to view an article.
    """

    id: str
    created_at: datetime
    title: str
    cover_image: str
    duration: str | None
    media: list[str] | None
    content: str
    author: ViewAuthorDetailsEntity
    category: str


class GetArticleEntity(BaseEntity):
    """
    Response to get an article.
    """

    id: str
    title: str
    cover_image: str
    author: GetAuthorEntity


class ListArticlesEntity(BaseEntity):
    """
    Response to list articles.
    """

    records: list[GetArticleEntity]


class ArticleCategoriesEntity(BaseEntity):
    """
    Response to list article categories.
    """

    id: str
    name: str


class ListArticleCategoriesEntity(BaseEntity):
    """
    Response to list article categories.
    """

    records: list[ArticleCategoriesEntity]
