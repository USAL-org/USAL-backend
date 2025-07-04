from typing import override
from uuid import UUID

from usal.core.enums.article import ArticleStatus, ArticleType
from usal.core.exceptions.api_exception import api_exception

from usal.domain.entities.article_entity import (
    ArticleCategoriesEntity,
    GetAdminArticleEntity,
    GetArticleEntity,
    ListAdminArticlesEntity,
    ListArticleCategoriesEntity,
    ListArticlesEntity,
    ViewArticleDetailsEntity,
)
from usal.domain.repositories.article_repo import ArticleRepo
from usal.infrastructure.queries.article import (
    create_article_async_edgeql,
    create_article_category_async_edgeql,
    get_all_articles_count_async_edgeql,
    get_article_by_id_async_edgeql,
    get_user_articles_count_async_edgeql,
    list_article_categories_async_edgeql,
    list_articles_async_edgeql,
    list_user_articles_async_edgeql,
)
from usal.infrastructure.repositories.pagination_repo import paginate


class DbArticleRepo(ArticleRepo):
    @override
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
        async with self.session() as session:
            article_obj = await create_article_async_edgeql.create_article(
                session,
                title=title,
                cover_image=cover_image,
                content=content,
                type=type,
                author=author,
                category=category,
                status=status,
                duration=duration,
                media=media,
            )
            if not article_obj:
                raise api_exception(
                    message="Unable to create article. Please try again.",
                )

    @override
    async def list_all_articles(
        self,
        page: int,
        limit: int,
        type: ArticleType | None = None,
        search: str | None = None,
    ) -> ListAdminArticlesEntity:
        async with self.session() as session:
            total_count = (
                await get_all_articles_count_async_edgeql.get_all_articles_count(
                    session,
                    search=search,
                    type=type,
                )
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_articles = await list_articles_async_edgeql.list_articles(
                session,
                type=type,
                offset=page_info.offset,
                limit=limit,
                search=search,
            )
            return ListAdminArticlesEntity(
                page_info=page_info,
                records=[
                    GetAdminArticleEntity.model_validate(article, from_attributes=True)
                    for article in db_articles
                ],
            )

    @override
    async def create_article_category(self, name: str) -> None:
        async with self.session() as session:
            category_obj = (
                await create_article_category_async_edgeql.create_article_category(
                    session,
                    name=name,
                )
            )
            if not category_obj:
                raise api_exception(
                    message="Unable to create article category. Please try again.",
                )

    @override
    async def list_all_article_categories(self) -> ListArticleCategoriesEntity:
        async with self.session() as session:
            db_categories = (
                await list_article_categories_async_edgeql.list_article_categories(
                    session,
                )
            )
            return ListArticleCategoriesEntity(
                records=[
                    ArticleCategoriesEntity.model_validate(
                        category, from_attributes=True
                    )
                    for category in db_categories
                ],
            )

    @override
    async def list_user_articles(
        self,
        page: int,
        limit: int,
        type: ArticleType,
        search: str | None = None,
    ) -> ListArticlesEntity:
        async with self.session() as session:
            total_count = (
                await get_user_articles_count_async_edgeql.get_user_articles_count(
                    session,
                    search=search,
                    type=type,
                )
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_articles = await list_user_articles_async_edgeql.list_user_articles(
                session,
                type=type,
                offset=page_info.offset,
                limit=limit,
                search=search,
            )
            return ListArticlesEntity(
                page_info=page_info,
                records=[
                    GetArticleEntity.model_validate(article, from_attributes=True)
                    for article in db_articles
                ],
            )

    @override
    async def get_article_by_id(self, article_id: UUID) -> ViewArticleDetailsEntity:
        async with self.session() as session:
            db_article = await get_article_by_id_async_edgeql.get_article_by_id(
                session,
                article_id=article_id,
            )
            if not db_article:
                raise api_exception(
                    message="Article not found.",
                )
            return ViewArticleDetailsEntity.model_validate(
                db_article, from_attributes=True
            )
