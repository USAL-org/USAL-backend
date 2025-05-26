from typing import Annotated

from fastapi import APIRouter, Depends
from wireup import Inject

from usal.api.schema.request.article_request import (
    AdminArticleFilterRequest,
    CreateArticleCategoryRequest,
    CreateArticleRequest,
)
from usal.api.schema.request.author_request import (
    CreateAuthorRequest,
    FilterAuthorRequest,
)
from usal.api.schema.request.qa_request import (
    AdminQAFilterRequest,
    CreateQARequest,
)
from usal.api.schema.request.resources_request import (
    AdminFilterResourcesRequest,
    CreateResourcesRequest,
)
from usal.api.schema.response.article_response import (
    ListAdminArticlesResponse,
    ListArticleCategoriesResponse,
)
from usal.api.schema.response.author_response import ListAuthorsResponse
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.qa_response import ListAdminQAResponse
from usal.api.schema.response.resources_response import (
    ListAdminResourcesResponse,
)
from usal.controllers.article_controller import ArticleController
from usal.controllers.author_controller import AuthorController
from usal.controllers.qa_controller import QAController
from usal.controllers.resources_controller import ResourcesController
from usal.core.api_response import APIResponse
from usal.core.permission_checker import AdminPermissions
from usal.util.perms import perms

AdminRouter = APIRouter(
    tags=["Admin"],
    prefix="/admin",
)


@AdminRouter.post("/author")
@perms(AdminPermissions.ARTICLE_MANAGEMENT)
async def create_author(
    request: CreateAuthorRequest,
    controller: Annotated[AuthorController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_author(request)


@AdminRouter.get("/authors")
@perms(AdminPermissions.ARTICLE_MANAGEMENT)
async def list_all_author(
    controller: Annotated[AuthorController, Inject()],
    filter: FilterAuthorRequest = Depends(FilterAuthorRequest),
) -> APIResponse[ListAuthorsResponse]:
    return await controller.list_all_author(
        filter=filter,
    )


@AdminRouter.post("/article/category")
@perms(AdminPermissions.ARTICLE_MANAGEMENT)
async def create_article_category(
    request: CreateArticleCategoryRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_article_category(request)


@AdminRouter.get("/article/categories")
@perms(AdminPermissions.ARTICLE_MANAGEMENT)
async def list_all_article_categories(
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[ListArticleCategoriesResponse]:
    return await controller.list_all_article_categories()


@AdminRouter.post("/article")
@perms(AdminPermissions.ARTICLE_MANAGEMENT)
async def create_article(
    request: CreateArticleRequest,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_article(request)


@AdminRouter.get("/articles")
@perms(AdminPermissions.ARTICLE_MANAGEMENT)
async def list_all_articles(
    controller: Annotated[ArticleController, Inject()],
    filter: AdminArticleFilterRequest = Depends(AdminArticleFilterRequest),
) -> APIResponse[ListAdminArticlesResponse]:
    return await controller.list_all_articles(filter)


@AdminRouter.post("/QA")
@perms(AdminPermissions.QA_MANAGEMENT)
async def create_QA(
    request: CreateQARequest,
    controller: Annotated[QAController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_qa(request)


@AdminRouter.get("/QAs")
@perms(AdminPermissions.QA_MANAGEMENT)
async def list_all_qa(
    controller: Annotated[QAController, Inject()],
    filter: AdminQAFilterRequest = Depends(AdminQAFilterRequest),
) -> APIResponse[ListAdminQAResponse]:
    return await controller.list_all_qa(filter=filter)


@AdminRouter.post("/resource")
@perms(AdminPermissions.RESOURCES_MANAGEMENT)
async def create_resource(
    request: CreateResourcesRequest,
    controller: Annotated[ResourcesController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.create_resources(request)


@AdminRouter.get("/resource")
@perms(AdminPermissions.RESOURCES_MANAGEMENT)
async def list_all_resources(
    controller: Annotated[ResourcesController, Inject()],
    filter: AdminFilterResourcesRequest = Depends(AdminFilterResourcesRequest),
) -> APIResponse[ListAdminResourcesResponse]:
    return await controller.list_all_resources(filter=filter)
