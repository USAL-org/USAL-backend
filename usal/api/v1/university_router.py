from typing import Annotated

from fastapi import APIRouter
from wireup import Inject

from usal.api.schema.request.university_request import (
    AddUniversityMajorRequest,
    AddUniversityRequest,
)
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.university_response import (
    ListStatesResponse,
    ListUniversitiesResponse,
    ListUniversityMajorsResponse,
)
from usal.controllers.university_controller import UniversityController
from usal.core.api_response import APIResponse

UniversityRouter = APIRouter(
    tags=["University Management"],
    prefix="/university",
)


@UniversityRouter.get("/states")
async def list_states(
    controller: Annotated[UniversityController, Inject()],
) -> APIResponse[ListStatesResponse]:
    return await controller.list_states()


@UniversityRouter.get("/majors")
async def list_university_majors(
    controller: Annotated[UniversityController, Inject()],
) -> APIResponse[ListUniversityMajorsResponse]:
    return await controller.list_university_majors()


@UniversityRouter.post("/majors")
async def add_university_major(
    request: AddUniversityMajorRequest,
    controller: Annotated[UniversityController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.add_university_major(request)


@UniversityRouter.post("")
async def add_university(
    request: AddUniversityRequest,
    controller: Annotated[UniversityController, Inject()],
) -> APIResponse[MessageResponse]:
    return await controller.add_university(request)


@UniversityRouter.get("")
async def list_all_universities(
    controller: Annotated[UniversityController, Inject()],
) -> APIResponse[ListUniversitiesResponse]:
    return await controller.list_universities()
