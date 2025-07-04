# AUTOGENERATED FROM 'usal/infrastructure/queries/university/list_universities.edgeql' WITH:
#     $ gel-py


from __future__ import annotations
import dataclasses
import enum
import gel
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema
        return any_schema()

    @classmethod
    def __get_validators__(cls):
        # Pydantic 1.x
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        _ = pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


class DegreeNames(enum.Enum):
    ASSOCIATES_DEGREE = "ASSOCIATES_DEGREE"
    BACHELORS_DEGREE = "BACHELORS_DEGREE"
    MASTERS_DEGREE = "MASTERS_DEGREE"
    DOCTORAL_DEGREE = "DOCTORAL_DEGREE"


@dataclasses.dataclass
class ListUniversitiesResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    location: str
    image: str
    state: ListUniversitiesResultState
    description: str | None
    acceptance_rate: float
    annual_fee: float
    student_faculty_ratio: str | None
    available_majors: list[ListUniversitiesResultAvailableMajorsItem]
    admission_requirements: list[str]
    status: UniversityStatus
    view_count: int | None
    degree: list[ListUniversitiesResultDegreeItem]
    url: str | None
    rating: float | None
    featured: bool


@dataclasses.dataclass
class ListUniversitiesResultAvailableMajorsItem(NoPydanticValidation):
    id: uuid.UUID
    name: str


@dataclasses.dataclass
class ListUniversitiesResultDegreeItem(NoPydanticValidation):
    id: uuid.UUID
    name: DegreeNames


@dataclasses.dataclass
class ListUniversitiesResultState(NoPydanticValidation):
    id: uuid.UUID
    name: str


class UniversityStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


async def list_universities(
    executor: gel.AsyncIOExecutor,
    *,
    search: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
) -> list[ListUniversitiesResult]:
    return await executor.query(
        """\
        WITH
            search := <optional str>$search,

        FILTERED_UNIVERSITY := (
            SELECT University
            FILTER (
            (.name ILIKE '%' ++ search ++ '%' IF EXISTS search ELSE TRUE)
            )
            ORDER BY .name ASC
            OFFSET <optional int64>$offset
            LIMIT <optional int64>$limit
        )
        SELECT FILTERED_UNIVERSITY {
            id,
            name,
            location,
            image,
            state:{
                id,
                name,
            },
            description,
            acceptance_rate,
            annual_fee,
            student_faculty_ratio,
            available_majors:{
                id,
                name,
            },
            admission_requirements,
            status,
            view_count,
            degree :{
                id,
                name,
            },
            url,
            rating, 
            featured,
        }\
        """,
        search=search,
        offset=offset,
        limit=limit,
    )
