from usal.api.schema.request.university_request import (
    AddUniversityMajorRequest,
    AddUniversityRequest,
)
from usal.domain.entities.university_entity import (
    ListStatesEntity,
    ListUniversitiesEntity,
    ListUniversityMajorsEntity,
)
from usal.domain.repositories.university_repo import UniversityRepo


class UniversityUsecase:
    def __init__(
        self,
        repo: UniversityRepo,
    ) -> None:
        self.repo = repo

    async def list_states(self) -> ListStatesEntity:
        return await self.repo.list_states()

    async def add_university_major(self, request: AddUniversityMajorRequest) -> None:
        return await self.repo.add_university_major(
            name=request.name,
        )

    async def list_university_majors(self) -> ListUniversityMajorsEntity:
        return await self.repo.list_university_majors()

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
        )

    async def list_universities(self) -> ListUniversitiesEntity:
        return await self.repo.list_universities()
