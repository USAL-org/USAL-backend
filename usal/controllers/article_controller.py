from uuid import UUID
from usal.api.schema.request.article_request import (
    ArticleFilterRequest,
    CreateArticleCategoryRequest,
    CreateArticleRequest,
)
from usal.api.schema.response.article_response import (
    ArticleCategoriesResponse,
    GetArticleResponse,
    ListArticleCategoriesResponse,
    ListArticlesResponse,
    ViewArticleDetailsResponse,
)
from usal.core.api_response import APIResponse, api_response
from usal.api.schema.response.common_response import MessageResponse


class ArticleController:
    def __init__(
        self,
        usecase: ArticleUsecase,
    ) -> None:
        self.usecase = usecase

    async def create_article(
        self,
        request: CreateArticleRequest,
    ) -> APIResponse[MessageResponse]:
        await self.usecase.create_article(
            request=request,
        )
        return api_response(MessageResponse(message="Article created successfully."))

    async def list_all_articles(
        self,
        filter: ArticleFilterRequest,
    ) -> APIResponse[ListArticlesResponse]:
        articles_obj = await self.usecase.list_all_articles(
            filter=filter,
        )
        return api_response(
            ListArticlesResponse(
                **articles_obj.page_info.model_dump(),
                records=[
                    GetArticleResponse.model_validate(article, from_attributes=True)
                    for article in articles_obj.records
                ],
            )
        )

    async def create_article_category(
        self,
        request: CreateArticleCategoryRequest,
    ) -> APIResponse[MessageResponse]:
        await self.usecase.create_article_category(
            request=request,
        )
        return api_response(
            MessageResponse(message="Article category created successfully.")
        )

    async def list_all_article_categories(
        self,
    ) -> APIResponse[ListArticleCategoriesResponse]:
        category_obj = await self.usecase.list_user_articles()
        return api_response(
            ListArticleCategoriesResponse(
                records=[
                    ArticleCategoriesResponse.model_validate(
                        category, from_attributes=True
                    )
                    for category in category_obj.records
                ],
            )
        )

    async def list_user_articles(
        self,
        filter: ArticleFilterRequest,
    ) -> APIResponse[ListArticlesResponse]:
        articles_obj = await self.usecase.list_user_articles(
            filter=filter,
        )
        return api_response(
            ListArticlesResponse(
                **articles_obj.page_info.model_dump(),
                records=[
                    GetArticleResponse.model_validate(article, from_attributes=True)
                    for article in articles_obj.records
                ],
            )
        )

    async def get_article_by_id(
        self,
        article_id: UUID,
    ) -> APIResponse[ViewArticleDetailsResponse]:
        articles_obj = await self.usecase.get_article_by_id(article_id=article_id)
        return api_response(
            ViewArticleDetailsResponse.model_validate(
                articles_obj,
                from_attributes=True,
            )
        )
