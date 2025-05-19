from uuid import UUID
from pydantic import Field
from usal.api.schema.request.common_request import PaginationRequest
from usal.core import BaseRequest
from usal.core.enums.article import ArticleStatus, ArticleType


class CreateArticleRequest(BaseRequest):
    """
    Request to create an article.
    """

    title: str = Field(description="Title of the article.")
    cover_image: str = Field(description="Cover image URL of the article.")
    duration: str | None = Field(
        None, description="Duration of the article in minutes."
    )
    media: list[str] | None = Field(
        None, description="List of media URLs related to the article."
    )
    content: str = Field(description="Content of the article.")
    type: ArticleType = Field(
        description="Type of the article. Can be either 'news' or 'blog'."
    )
    author: UUID = Field(description="UUID of the author.")
    category: UUID = Field(description="UUID of the category.")
    status: ArticleStatus = Field(
        description="Status of the article. Can be either 'active' or 'inactive'."
    )


class CreateArticleCategoryRequest(BaseRequest):
    """
    Request to create an article category.
    """

    name: str = Field(description="Name of the article category.")


class ArticleFilterRequest(PaginationRequest):
    """
    Request to filter articles.
    """

    search: str | None = Field(None, description="Title of the article.")
    type: ArticleType = Field(
        description="Type of the article. Can be either 'news' or 'blog'."
    )
