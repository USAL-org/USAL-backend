from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from wireup import Inject

from usal.api.schema.request.article_request import (
    ArticleFilterRequest,
)
from usal.api.schema.response.article_response import (
    ListArticlesResponse,
    ViewArticleDetailsResponse,
)
from usal.api.schema.response.qa_response import ListQAResponse
from usal.api.schema.response.resources_response import ListResourcesResponse
from usal.api.schema.response.university_response import ListUniversitiesResponse
from usal.controllers.article_controller import ArticleController
from usal.controllers.qa_controller import QAController
from usal.controllers.resources_controller import ResourcesController
from usal.controllers.university_controller import UniversityController
from usal.core.api_response import APIResponse
from usal.core.enums.qa import QAType

UserRouter = APIRouter(
    tags=["User"],
    prefix="/user",
)


@UserRouter.get("/articles")
async def list_articles(
    controller: Annotated[ArticleController, Inject()],
    filter: ArticleFilterRequest = Depends(ArticleFilterRequest),
) -> APIResponse[ListArticlesResponse]:
    return await controller.list_user_articles(filter)


@UserRouter.get("/article/{id}")
async def get_article_by_id(
    id: UUID,
    controller: Annotated[ArticleController, Inject()],
) -> APIResponse[ViewArticleDetailsResponse]:
    return await controller.get_article_by_id(article_id=id)


@UserRouter.get("/QAs")
async def list_all_qa(
    type: QAType,
    controller: Annotated[QAController, Inject()],
) -> APIResponse[ListQAResponse]:
    return await controller.list_all_qa(type)


@UserRouter.get("/resource")
async def list_all_resources(
    controller: Annotated[ResourcesController, Inject()],
) -> APIResponse[ListResourcesResponse]:
    return await controller.list_all_resources()


@UserRouter.get("/universities")
async def list_all_universities(
    controller: Annotated[UniversityController, Inject()],
) -> APIResponse[ListUniversitiesResponse]:
    return await controller.list_universities()
