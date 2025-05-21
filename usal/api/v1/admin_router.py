from typing import Annotated

from fastapi import APIRouter, Depends
from wireup import Inject

from usal.api.schema.request.article_request import (
    ArticleFilterRequest,
    CreateArticleCategoryRequest,
    CreateArticleRequest,
)
from usal.api.schema.request.author_request import CreateAuthorRequest
from usal.api.schema.request.qa_request import CreateQARequest
from usal.api.schema.request.resources_request import CreateResourcesRequest
from usal.api.schema.response.article_response import (
    ListArticleCategoriesResponse,
    ListArticlesResponse,
)
from usal.api.schema.response.author_response import ListAuthorsResponse
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.qa_response import ListQAResponse
from usal.api.schema.response.resources_response import ListResourcesResponse
from usal.controllers.article_controller import ArticleController
from usal.controllers.author_controller import AuthorController
from usal.controllers.qa_controller import QAController
from usal.controllers.resources_controller import ResourcesController
from usal.core.api_response import APIResponse
from usal.core.enums.qa import QAType

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


@AdminRouter.get("/authors")
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


@AdminRouter.get("/articles")
async def list_all_articles(
    controller: Annotated[ArticleController, Inject()],
    filter: ArticleFilterRequest = Depends(ArticleFilterRequest),
) -> APIResponse[ListArticlesResponse]:
    return await controller.list_all_articles(filter)


@AdminRouter.post("/article/category")
async def create_article_category(
    request: CreateArticleCategoryRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_article_category(request)


@AdminRouter.get("/article/categories")
async def list_all_article_categories(
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[ListArticleCategoriesResponse]:
    return await controller.list_all_article_categories()


@AdminRouter.post("/QA")
async def create_QA(
    request: CreateQARequest,
    controller: Annotated[QAController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_qa(request)


@AdminRouter.get("/QAs")
async def list_all_qa(
    type: QAType,
    controller: Annotated[QAController, Inject()],
) -> APIResponse[ListQAResponse]:
    return await controller.list_all_qa(type)


@AdminRouter.post("/resource")
async def create_resource(
    request: CreateResourcesRequest,
    controller: Annotated[ResourcesController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_resources(request)


@AdminRouter.get("/resource")
async def list_all_resources(
    controller: Annotated[ResourcesController, Inject()],
) -> APIResponse[ListResourcesResponse]:
    return await controller.list_all_resources()
