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
    ListUniversityDegreesEntity,
    ListUniversityMajorsEntity,
    StateEntity,
    UniversityDegreeEntity,
    UniversityMajorEntity,
)
from usal.domain.repositories.university_repo import UniversityRepo
from usal.infrastructure.queries.university import (
    add_uni_major_async_edgeql,
    add_university_async_edgeql,
    get_all_uni_count_async_edgeql,
    get_featured_uni_count_async_edgeql,
    get_match_uni_count_async_edgeql,
    get_user_uni_count_async_edgeql,
    increase_view_count_async_edgeql,
    list_degrees_async_edgeql,
    list_featured_universities_async_edgeql,
    list_states_async_edgeql,
    list_uni_majors_async_edgeql,
    list_universities_async_edgeql,
    list_user_university_async_edgeql,
    match_university_list_async_edgeql,
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
    async def list_university_degrees(self) -> ListUniversityDegreesEntity:
        async with self.session() as session:
            db_university_degrees = await list_degrees_async_edgeql.list_degrees(
                session,
            )
            return ListUniversityDegreesEntity(
                records=[
                    UniversityDegreeEntity.model_validate(degree, from_attributes=True)
                    for degree in db_university_degrees
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
        acceptance_rate: float,
        annual_fee: float,
        student_faculty_ratio: str,
        available_majors: list[UUID],
        admission_requirements: list[str],
        status: UniversityStatus,
        degrees: list[UUID],
        rating: float,
        url: str,
        featured: bool,
        test_required: bool,
        min_gpa: float,
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
                degrees=degrees,
                rating=rating,
                url=url,
                featured=featured,
                min_gpa=min_gpa,
                test_required=test_required,
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
                    "degree": university.degree,
                    "url": university.url,
                    "rating": university.rating,
                    "featured": university.featured,
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
        degree: UUID | None = None,
        application_fee: bool | None = None,
        community_college: bool | None = None,
    ) -> ListUniversitiesEntity:
        async with self.session() as session:
            total_count = await get_user_uni_count_async_edgeql.get_user_uni_count(
                session,
                search=search,
                state=state,
                major=major,
                degree=degree,
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
                    degree=degree,
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
                    "degree": university.degree,
                    "url": university.url,
                    "rating": university.rating,
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

    @override
    async def list_featured_universities(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        state: UUID | None = None,
        major: UUID | None = None,
        degree: UUID | None = None,
        application_fee: bool | None = None,
        community_college: bool | None = None,
    ) -> ListUniversitiesEntity:
        async with self.session() as session:
            total_count = (
                await get_featured_uni_count_async_edgeql.get_featured_uni_count(
                    session,
                    search=search,
                    state=state,
                    major=major,
                    degree=degree,
                    application_fee=application_fee,
                    community_college=community_college,
                )
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_universities = await list_featured_universities_async_edgeql.list_featured_universities(
                session,
                offset=page_info.offset,
                limit=limit,
                search=search,
                state=state,
                major=major,
                application_fee=application_fee,
                community_college=community_college,
                degree=degree,
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
                    "degree": university.degree,
                    "url": university.url,
                    "rating": university.rating,
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

    @override
    async def visit_university(self, university_id: UUID) -> None:
        async with self.session() as session:
            db_university = await increase_view_count_async_edgeql.increase_view_count(
                session,
                university_id=university_id,
            )
            if not db_university:
                raise api_exception(
                    message="Unable to visit university. Please try again.",
                )

    @override
    async def match_university(
        self,
        page: int,
        limit: int,
        major: UUID,
        degree: UUID,
        min_gpa: float,
        test_required: bool,
        min_fee: float,
        max_fee: float,
    ) -> ListUniversitiesEntity:
        async with self.session() as session:
            total_count = await get_match_uni_count_async_edgeql.get_match_uni_count(
                session,
                major=major,
                degree=degree,
                min_gpa=min_gpa,
                test_required=test_required,
                min_fee=min_fee,
                max_fee=max_fee,
            )
            page_info = await paginate(total_count.total_count, page, limit)
            db_universities = (
                await match_university_list_async_edgeql.match_university_list(
                    session,
                    offset=page_info.offset,
                    limit=limit,
                    major=major,
                    degree=degree,
                    min_gpa=min_gpa,
                    test_required=test_required,
                    min_fee=min_fee,
                    max_fee=max_fee,
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
                    "degree": university.degree,
                    "url": university.url,
                    "rating": university.rating,
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
