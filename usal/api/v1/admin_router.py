from typing import Annotated

from fastapi import APIRouter
from wireup import Inject

from usal.api.schema.request.article_request import (
    CreateArticleCategoryRequest,
    CreateArticleRequest,
)
from usal.api.schema.request.author_request import CreateAuthorRequest
from usal.api.schema.response.common_response import MessageResponse
from usal.core.api_response import APIResponse

AdminRouter = APIRouter(
    tags=["Admin"],
    prefix="/admin",
)


@AdminRouter.post("/author")
async def create_author(
    request: CreateAuthorRequest,
    controller: Annotated[AdminController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_author(request)


@AdminRouter.post("/article")
async def create_article(
    request: CreateArticleRequest,
    controller: Annotated[AdminController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.add_article(request)


@AdminRouter.post("/article/category")
async def create_article_category(
    request: CreateArticleCategoryRequest,
    controller: Annotated[AdminController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_article_category(request)
