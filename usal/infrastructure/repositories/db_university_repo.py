from typing import override
from uuid import UUID
from usal.core.enums.university import UniversityStatus
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.university_entity import (
    GetUniversityEntity,
    ListStatesEntity,
    ListUniversitiesEntity,
    ListUniversityMajorsEntity,
    StateEntity,
    UniversityMajorEntity,
)
from usal.domain.repositories.university_repo import UniversityRepo
from usal.infrastructure.queries.university import (
    add_uni_major_async_edgeql,
    add_university_async_edgeql,
    list_states_async_edgeql,
    list_uni_majors_async_edgeql,
    list_universities_async_edgeql,
)


class DbUniversityRepo(UniversityRepo):
    @override
    async def list_states(self) -> ListStatesEntity:
        async with self.session() as session:
            db_states = await list_states_async_edgeql.list_states(session)
            return ListStatesEntity(
                records=[
                    StateEntity.model_validate(state, from_attributes=True)
                    for state in db_states
                ],
            )

    @override
    async def add_university_major(
        self,
        name: str,
    ) -> None:
        async with self.session() as session:
            db_university_major = await add_uni_major_async_edgeql.add_uni_major(
                session,
                name=name,
            )
            if not db_university_major:
                raise api_exception(
                    message="Unable to add university major. Please try again.",
                )

    @override
    async def list_university_majors(self) -> ListUniversityMajorsEntity:
        async with self.session() as session:
            db_university_majors = await list_uni_majors_async_edgeql.list_uni_majors(
                session,
            )
            return ListUniversityMajorsEntity(
                records=[
                    UniversityMajorEntity.model_validate(major, from_attributes=True)
                    for major in db_university_majors
                ],
            )

    @override
    async def add_university(
        self,
        name: str,
        location: str,
        image: str,
        application_fee: bool,
        community_college: bool,
        state: UUID,
        description: str,
        acceptance_rate: str,
        annual_fee: str,
        student_faculty_ratio: str,
        available_majors: list[UUID],
        admission_requirements: list[str],
        status: UniversityStatus,
    ) -> None:
        async with self.session() as session:
            db_university = await add_university_async_edgeql.add_university(
                session,
                name=name,
                location=location,
                image=image,
                application_fee=application_fee,
                community_college=community_college,
                state=state,
                description=description,
                acceptance_rate=acceptance_rate,
                annual_fee=annual_fee,
                student_faculty_ratio=student_faculty_ratio,
                available_majors=available_majors,
                admission_requirements=admission_requirements,
                status=status,
            )
            if not db_university:
                raise api_exception(
                    message="Unable to add university. Please try again.",
                )

    @override
    async def list_universities(self) -> ListUniversitiesEntity:
        async with self.session() as session:
            db_universities = await list_universities_async_edgeql.list_universities(
                session,
            )
            return ListUniversitiesEntity(
                records=[
                    GetUniversityEntity.model_validate(university, from_attributes=True)
                    for university in db_universities
                ],
            )
