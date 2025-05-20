from abc import abstractmethod
from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.core.enums.article import ArticleStatus, ArticleType
from usal.domain.entities.article_entity import (
    ListArticleCategoriesEntity,
    ListArticlesEntity,
    ViewArticleDetailsEntity,
)


class ArticleRepo(DbRepo):
    @abstractmethod
    async def create_article(
        self,
        title: str,
        cover_image: str,
        content: str,
        type: ArticleType,
        author: UUID,
        category: UUID,
        status: ArticleStatus,
        duration: str | None = None,
        media: list[str] | None = None,
    ) -> None:
        """
        Create an article.

        Parameters:
            title (str): Title of the article.
            cover_image (str): Cover image URL of the article.
            content (str): Content of the article.
            type (ArticleType): Type of the article. Can be either 'news' or 'blog'.
            author (UUID): UUID of the author.
            category (UUID): UUID of the category.
            status (ArticleStatus): Status of the article. Can be either 'active' or 'inactive'.
            duration (str | None): Duration of the article in minutes.
            media (list[str] | None): List of media URLs related to the article.

        Returns:
            None
        """

    # @abstractmethod
    # async def update_article(
    #     self,
    #     article_id: UUID,
    #     title: str | None = None,
    #     cover_image: str | None = None,
    #     content: str | None = None,
    #     type: ArticleType | None = None,
    #     author: UUID | None = None,
    #     category: UUID | None = None,
    #     status: ArticleStatus | None = None,
    #     duration: str | None = None,
    #     media: list[str] | None = None,
    # ) -> None:
    #     """
    #     Update an article.
    #     Parameters:
    #         article_id (UUID): ID of the article.
    #         title (str | None): Title of the article.
    #         cover_image (str | None): Cover image URL of the article.
    #         content (str | None): Content of the article.
    #         type (ArticleType | None): Type of the article. Can be either 'news' or 'blog'.
    #         author (UUID | None): UUID of the author.
    #         category (UUID | None): UUID of the category.
    #         status (ArticleStatus | None): Status of the article. Can be either 'active' or 'inactive'.
    #         duration (str | None): Duration of the article in minutes.
    #         media (list[str] | None): List of media URLs related to the article.
    #     Returns:
    #         None
    #     """

    @abstractmethod
    async def list_all_articles(self, type: ArticleType) -> ListArticlesEntity:
        """
        List all articles.

        Returns:
            ListArticlesEntity: List of articles.
        """

    @abstractmethod
    async def create_article_category(
        self,
        name: str,
    ) -> None:
        """
        Create an article category.

        Parameters:
            name (str): Name of the article category.

        Returns:
            None
        """

    # @abstractmethod
    # async def update_article_category(
    #     self,
    #     category_id: UUID,
    #     name: str | None = None,
    # ) -> None:
    #     """
    #     Update an article category.

    #     Parameters:
    #         category_id (UUID): ID of the article category.
    #         name (str | None): Name of the article category.

    #     Returns:
    #         None
    #     """

    @abstractmethod
    async def list_all_article_categories(self) -> ListArticleCategoriesEntity:
        """
        List all article categories.

        Returns:
            ListArticleCategoriesEntity: List of article categories.
        """

    @abstractmethod
    async def list_user_articles(self, type: ArticleType) -> ListArticlesEntity:
        """
        List all articles.

        Returns:
            ListArticlesEntity: List of articles.
        """

    @abstractmethod
    async def get_article_by_id(
        self,
        article_id: UUID,
    ) -> ViewArticleDetailsEntity:
        """
        Get an article by ID.

        Parameters:
            article_id (UUID): ID of the article.

        Returns:
            ViewArticleDetailsEntity: Article details.
        """
