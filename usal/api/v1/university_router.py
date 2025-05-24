from typing import Annotated

from fastapi import APIRouter, Depends
from wireup import Inject

from usal.api.schema.request.university_request import (
    AddUniversityMajorRequest,
    AddUniversityRequest,
    AdminUniversityFilterRequest,
    MajorAndStateFilterRequest,
)
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.university_response import (
    ListAdminUniversitiesResponse,
    ListStatesResponse,
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
    filter: MajorAndStateFilterRequest = Depends(MajorAndStateFilterRequest),
) -> APIResponse[ListStatesResponse]:
    return await controller.list_states(filter)


@UniversityRouter.get("/majors")
async def list_university_majors(
    controller: Annotated[UniversityController, Inject()],
    filter: MajorAndStateFilterRequest = Depends(MajorAndStateFilterRequest),
) -> APIResponse[ListUniversityMajorsResponse]:
    return await controller.list_university_majors(filter)


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
    filter: AdminUniversityFilterRequest = Depends(AdminUniversityFilterRequest),
) -> APIResponse[ListAdminUniversitiesResponse]:
    return await controller.list_universities(filter)
