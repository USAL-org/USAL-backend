from typing import Annotated

from fastapi import APIRouter
from wireup import Inject

from usal.api.schema.request.article_request import (
    ArticleFilterRequest,
    CreateArticleCategoryRequest,
    CreateArticleRequest,
)
from usal.api.schema.request.author_request import CreateAuthorRequest
from usal.api.schema.response.article_response import (
    ListArticleCategoriesResponse,
    ListArticlesResponse,
)
from usal.api.schema.response.author_response import ListAuthorsResponse
from usal.api.schema.response.common_response import MessageResponse
from usal.controllers.article_controller import ArticleController
from usal.controllers.author_controller import AuthorController
from usal.core.api_response import APIResponse

AdminRouter = APIRouter(
    tags=["Admin"],
    prefix="/admin",
)


@AdminRouter.post("/author")
async def create_author(
    request: CreateAuthorRequest,
    controller: Annotated[AuthorController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_author(request)


@AdminRouter.get("/author")
async def list_all_author(
    controller: Annotated[AuthorController, Inject()],
) -> APIResponse[ListAuthorsResponse]:
    return await controller.list_all_author()


@AdminRouter.post("/article")
async def create_article(
    request: CreateArticleRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_article(request)


@AdminRouter.get("/article")
async def list_all_articles(
    filter: ArticleFilterRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[ListArticlesResponse]:
    return await controller.list_all_articles(filter)


@AdminRouter.post("/article/category")
async def create_article_category(
    request: CreateArticleCategoryRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_article_category(request)


@AdminRouter.get("/article/category")
async def list_all_article_categories(
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[ListArticleCategoriesResponse]:
    return await controller.list_all_article_categories()
