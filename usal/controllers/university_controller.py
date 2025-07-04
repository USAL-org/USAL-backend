from usal.api.schema.request.university_request import (
    AddUniversityMajorRequest,
    AddUniversityRequest,
    AdminUniversityFilterRequest,
    MajorAndStateFilterRequest,
    UniversityFilterRequest,
)
from usal.api.schema.response.common_response import MessageResponse
from usal.api.schema.response.university_response import (
    GetAdminUniversityResponse,
    GetUniversityResponse,
    ListAdminUniversitiesResponse,
    ListStatesResponse,
    ListUniversitiesResponse,
    ListUniversityDegreesResponse,
    ListUniversityMajorsResponse,
    StateResponse,
    UniversityDegreeResponse,
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
        filter: MajorAndStateFilterRequest,
    ) -> APIResponse[ListStatesResponse]:
        states_obj = await self.usecase.list_states(filter)
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
        self, filter: MajorAndStateFilterRequest
    ) -> APIResponse[ListUniversityMajorsResponse]:
        majors_obj = await self.usecase.list_university_majors(filter)
        return api_response(
            ListUniversityMajorsResponse(
                records=[
                    UniversityMajorResponse.model_validate(major, from_attributes=True)
                    for major in majors_obj.records
                ],
            )
        )

    async def list_university_degrees(
        self,
    ) -> APIResponse[ListUniversityDegreesResponse]:
        degrees_obj = await self.usecase.list_university_degrees()
        return api_response(
            ListUniversityDegreesResponse(
                records=[
                    UniversityDegreeResponse.model_validate(
                        degree, from_attributes=True
                    )
                    for degree in degrees_obj.records
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
        filter: AdminUniversityFilterRequest,
    ) -> APIResponse[ListAdminUniversitiesResponse]:
        universities_obj = await self.usecase.list_universities(filter)
        return api_response(
            ListAdminUniversitiesResponse(
                **universities_obj.page_info.model_dump(),
                records=[
                    GetAdminUniversityResponse.model_validate(
                        university, from_attributes=True
                    )
                    for university in universities_obj.records
                ],
            )
        )

    async def list_user_universities(
        self,
        filter: UniversityFilterRequest,
    ) -> APIResponse[ListUniversitiesResponse]:
        universities_obj = await self.usecase.list_user_universities(filter)
        return api_response(
            ListUniversitiesResponse(
                **universities_obj.page_info.model_dump(),
                records=[
                    GetUniversityResponse.model_validate(
                        university, from_attributes=True
                    )
                    for university in universities_obj.records
                ],
            )
        )

    async def list_featured_universities(
        self,
        filter: UniversityFilterRequest,
    ) -> APIResponse[ListUniversitiesResponse]:
        universities_obj = await self.usecase.list_featured_universities(filter)
        return api_response(
            ListUniversitiesResponse(
                **universities_obj.page_info.model_dump(),
                records=[
                    GetUniversityResponse.model_validate(
                        university, from_attributes=True
                    )
                    for university in universities_obj.records
                ],
            )
        )
