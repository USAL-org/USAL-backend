from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from wireup import Inject

from usal.api.schema.request.article_request import (
    ArticleFilterRequest,
)
from usal.api.schema.response.article_response import (
    ListArticlesResponse,
    ViewArticleDetailsResponse,
)
from usal.controllers.article_controller import ArticleController
from usal.core.api_response import APIResponse

ArticleRouter = APIRouter(
    tags=["Articles"],
    prefix="/article",
)


@ArticleRouter.get("")
async def list_articles(
    filter: ArticleFilterRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[ListArticlesResponse]:
    return await controller.list_user_articles(filter)


@ArticleRouter.get("/{id}")
async def get_article_by_id(
    id: UUID,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[ViewArticleDetailsResponse]:
    return await controller.get_article_by_id(article_id=id)
