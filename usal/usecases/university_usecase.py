from usal.api.schema.request.university_request import (
    AddUniversityMajorRequest,
    AddUniversityRequest,
    AdminUniversityFilterRequest,
    MajorAndStateFilterRequest,
    UniversityFilterRequest,
)
from usal.domain.entities.university_entity import (
    GetAdminUniversityEntity,
    GetUniversityEntity,
    ListAdminUniversitiesEntity,
    ListStatesEntity,
    ListUniversitiesEntity,
    ListUniversityDegreesEntity,
    ListUniversityMajorsEntity,
)
from usal.domain.repositories.university_repo import UniversityRepo


class UniversityUsecase:
    def __init__(
        self,
        repo: UniversityRepo,
    ) -> None:
        self.repo = repo

    async def list_states(
        self,
        filter: MajorAndStateFilterRequest,
    ) -> ListStatesEntity:
        return await self.repo.list_states(search=filter.search)

    async def add_university_major(self, request: AddUniversityMajorRequest) -> None:
        return await self.repo.add_university_major(
            name=request.name,
        )

    async def list_university_majors(
        self,
        filter: MajorAndStateFilterRequest,
    ) -> ListUniversityMajorsEntity:
        return await self.repo.list_university_majors(search=filter.search)

    async def list_university_degrees(
        self,
    ) -> ListUniversityDegreesEntity:
        return await self.repo.list_university_degrees()

    async def add_university(self, request: AddUniversityRequest) -> None:
        return await self.repo.add_university(
            name=request.name,
            location=request.location,
            image=request.image,
            application_fee=request.application_fee,
            community_college=request.community_college,
            state=request.state,
            description=request.description,
            acceptance_rate=request.acceptance_rate,
            annual_fee=request.annual_fee,
            student_faculty_ratio=request.student_faculty_ratio,
            available_majors=request.available_majors,
            admission_requirements=request.admission_requirements,
            status=request.status,
            degrees=request.degrees,
            rating=request.rating,
            url=request.url,
            featured=request.featured,
        )

    async def list_universities(
        self,
        filter: AdminUniversityFilterRequest,
    ) -> ListAdminUniversitiesEntity:
        uni_obj = await self.repo.list_universities(
            search=filter.search,
            page=filter.page,
            limit=filter.limit,
        )
        return ListAdminUniversitiesEntity(
            page_info=uni_obj.page_info,
            records=[
                GetAdminUniversityEntity.model_validate(
                    university,
                    from_attributes=True,
                )
                for university in uni_obj.records
            ],
        )

    async def list_user_universities(
        self,
        filter: UniversityFilterRequest,
    ) -> ListUniversitiesEntity:
        uni_obj = await self.repo.list_user_universities(
            search=filter.search,
            page=filter.page,
            limit=filter.limit,
            state=filter.state,
            major=filter.major,
            degree=filter.degree,
            application_fee=filter.application_fee,
            community_college=filter.community_college,
        )
        return ListUniversitiesEntity(
            page_info=uni_obj.page_info,
            records=[
                GetUniversityEntity.model_validate(
                    university,
                    from_attributes=True,
                )
                for university in uni_obj.records
            ],
        )

    async def list_featured_universities(
        self,
        filter: UniversityFilterRequest,
    ) -> ListUniversitiesEntity:
        uni_obj = await self.repo.list_featured_universities(
            search=filter.search,
            page=filter.page,
            limit=filter.limit,
            state=filter.state,
            major=filter.major,
            degree=filter.degree,
            application_fee=filter.application_fee,
            community_college=filter.community_college,
        )
        return ListUniversitiesEntity(
            page_info=uni_obj.page_info,
            records=[
                GetUniversityEntity.model_validate(
                    university,
                    from_attributes=True,
                )
                for university in uni_obj.records
            ],
        )
