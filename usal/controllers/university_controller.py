from usal.api.schema.request.university_request import (
    AddUniversityMajorRequest,
    AddUniversityRequest,
)
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.university_response import (
    GetUniversityResponse,
    ListStatesResponse,
    ListUniversitiesResponse,
    ListUniversityMajorsResponse,
    StateResponse,
    UniversityMajorResponse,
)
from usal.core.api_response import APIResponse, api_response
from usal.usecases.university_usecase import UniversityUsecase


class UniversityController:
    def __init__(
        self,
        usecase: UniversityUsecase,
    ) -> None:
        self.usecase = usecase

    async def list_states(
        self,
    ) -> APIResponse[ListStatesResponse]:
        states_obj = await self.usecase.list_states()
        return api_response(
            ListStatesResponse(
                records=[
                    StateResponse.model_validate(state, from_attributes=True)
                    for state in states_obj.records
                ],
            )
        )

    async def add_university_major(
        self,
        request: AddUniversityMajorRequest,
    ) -> APIResponse[MessageResponse]:
        await self.usecase.add_university_major(request=request)
        return api_response(
            MessageResponse(message="University major added successfully")
        )

    async def list_university_majors(
        self,
    ) -> APIResponse[ListUniversityMajorsResponse]:
        majors_obj = await self.usecase.list_university_majors()
        return api_response(
            ListUniversityMajorsResponse(
                records=[
                    UniversityMajorResponse.model_validate(major, from_attributes=True)
                    for major in majors_obj.records
                ],
            )
        )

    async def add_university(
        self,
        request: AddUniversityRequest,
    ) -> APIResponse[MessageResponse]:
        await self.usecase.add_university(request=request)
        return api_response(MessageResponse(message="University added successfully"))

    async def list_universities(
        self,
    ) -> APIResponse[ListUniversitiesResponse]:
        universities_obj = await self.usecase.list_universities()
        return api_response(
            ListUniversitiesResponse(
                records=[
                    GetUniversityResponse.model_validate(
                        university, from_attributes=True
                    )
                    for university in universities_obj.records
                ],
            )
        )
