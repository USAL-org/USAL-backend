from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from wireup import Inject

from usal.api.schema.request.article_request import (
    CreateArticleCategoryRequest,
    CreateArticleRequest,
)
from usal.core.api_response import APIResponse

ArticleRouter = APIRouter(
    tags=["Articles"],
    prefix="/article",
)


@ArticleRouter.get("")
async def list_articles(
    filter: CreateArticleRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.add_article(filter)


@ArticleRouter.get("")
async def list_articles(
    filter: CreateArticleRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.add_article(filter)


@ArticleRouter.get("/{id}")
async def get_article_by_id(
    id: UUID,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_article_category(article_id=id)
