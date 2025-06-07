from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from wireup import Inject

from usal.api.schema.request.article_request import (
    ArticleFilterRequest,
)
from usal.api.schema.request.qa_request import QAFilterRequest
from usal.api.schema.request.resources_request import FilterResourcesRequest
from usal.api.schema.request.university_request import UniversityFilterRequest
from usal.api.schema.response.article_response import (
    ListArticlesResponse,
    ViewArticleDetailsResponse,
)
from usal.api.schema.response.qa_response import ListQAResponse, ViewQAResponse
from usal.api.schema.response.resources_response import ListResourcesResponse
from usal.api.schema.response.university_response import ListUniversitiesResponse
from usal.controllers.article_controller import ArticleController
from usal.controllers.qa_controller import QAController
from usal.controllers.resources_controller import ResourcesController
from usal.controllers.university_controller import UniversityController
from usal.core.api_response import APIResponse
from usal.core.jwt.jwt_bearer import JWTBearer
from usal.core.jwt.jwt_payload import JWTPayload

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
    controller: Annotated[QAController, Inject()],
    filter: QAFilterRequest = Depends(QAFilterRequest),
) -> APIResponse[ListQAResponse]:
    return await controller.list_user_qa(filter)


@UserRouter.get("/QA/{id}")
async def get_qa_by_id(
    id: UUID,
    controller: Annotated[QAController, Inject()],
    payload: JWTPayload = Depends(JWTBearer("user")),
) -> APIResponse[ViewQAResponse]:
    return await controller.get_qa_by_id(qa_id=id)


@UserRouter.get("/resource")
async def list_all_resources(
    controller: Annotated[ResourcesController, Inject()],
    filter: FilterResourcesRequest = Depends(FilterResourcesRequest),
) -> APIResponse[ListResourcesResponse]:
    return await controller.list_user_resources(filter)


@UserRouter.get("/universities")
async def list_all_universities(
    controller: Annotated[UniversityController, Inject()],
    filter: UniversityFilterRequest = Depends(UniversityFilterRequest),
) -> APIResponse[ListUniversitiesResponse]:
    return await controller.list_user_universities(filter)
