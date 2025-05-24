from typing import override
from uuid import UUID
from usal.core.enums.university import UniversityStatus
from usal.core.exceptions.api_exception import api_exception
from usal.domain.entities.university_entity import (
    GetAdminUniversityEntity,
    GetUniversityEntity,
    ListAdminUniversitiesEntity,
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
    get_all_uni_count_async_edgeql,
    get_user_uni_count_async_edgeql,
    list_states_async_edgeql,
    list_uni_majors_async_edgeql,
    list_universities_async_edgeql,
    list_user_university_async_edgeql,
)
from usal.infrastructure.repositories.pagination_repo import paginate


class DbUniversityRepo(UniversityRepo):
    @override
    async def list_states(
        self,
        search: str | None = None,
    ) -> ListStatesEntity:
        async with self.session() as session:
            db_states = await list_states_async_edgeql.list_states(
                session,
                search=search,
            )
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
    async def list_university_majors(
        self,
        search: str | None = None,
    ) -> ListUniversityMajorsEntity:
        async with self.session() as session:
            db_university_majors = await list_uni_majors_async_edgeql.list_uni_majors(
                session,
                search=search,
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
    async def list_universities(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> ListAdminUniversitiesEntity:
        async with self.session() as session:
            total_count = await get_all_uni_count_async_edgeql.get_all_uni_count(
                session,
                search=search,
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_universities = await list_universities_async_edgeql.list_universities(
                session,
                offset=page_info.offset,
                limit=limit,
                search=search,
            )
            university_entity = []
            for university in db_universities:
                university_dict = {
                    "id": university.id,
                    "name": university.name,
                    "location": university.location,
                    "image": university.image,
                    "state": university.state.name,
                    "description": university.description,
                    "acceptance_rate": university.acceptance_rate,
                    "annual_fee": university.annual_fee,
                    "student_faculty_ratio": university.student_faculty_ratio,
                    "available_majors": university.available_majors,
                    "admission_requirements": university.admission_requirements,
                    "view_count": university.view_count,
                    "status": university.status,
                }
                university_entity.append(
                    GetAdminUniversityEntity.model_validate(
                        university_dict, from_attributes=True
                    )
                )
            return ListAdminUniversitiesEntity(
                page_info=page_info,
                records=university_entity,
            )

    @override
    async def list_user_universities(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        state: UUID | None = None,
        major: UUID | None = None,
        application_fee: bool | None = None,
        community_college: bool | None = None,
    ) -> ListUniversitiesEntity:
        async with self.session() as session:
            total_count = await get_user_uni_count_async_edgeql.get_user_uni_count(
                session,
                search=search,
                state=state,
                major=major,
                application_fee=application_fee,
                community_college=community_college,
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_universities = (
                await list_user_university_async_edgeql.list_user_university(
                    session,
                    offset=page_info.offset,
                    limit=limit,
                    search=search,
                    state=state,
                    major=major,
                    application_fee=application_fee,
                    community_college=community_college,
                )
            )
            university_entity = []
            for university in db_universities:
                university_dict = {
                    "id": university.id,
                    "name": university.name,
                    "location": university.location,
                    "image": university.image,
                    "state": university.state.name,
                    "description": university.description,
                    "acceptance_rate": university.acceptance_rate,
                    "annual_fee": university.annual_fee,
                    "student_faculty_ratio": university.student_faculty_ratio,
                    "available_majors": university.available_majors,
                    "admission_requirements": university.admission_requirements,
                }
                university_entity.append(
                    GetUniversityEntity.model_validate(
                        university_dict, from_attributes=True
                    )
                )
            return ListUniversitiesEntity(
                page_info=page_info,
                records=university_entity,
            )
