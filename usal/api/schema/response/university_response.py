from uuid import UUID

from usal.core import BaseSchema, PaginatedSchema
from usal.core.enums.university import UniversityStatus


class UniversityMajorResponse(BaseSchema):
    """
    Response schema for university majors.
    """

    id: UUID
    name: str


class ListUniversityMajorsResponse(BaseSchema):
    """
    Response schema for listing university majors.
    """

    records: list[UniversityMajorResponse]


class UniversityDegreeResponse(BaseSchema):
    """
    Response schema for university degrees.
    """

    id: UUID
    name: str


class ListUniversityDegreesResponse(BaseSchema):
    """
    Response schema for listing university degrees.
    """

    records: list[UniversityDegreeResponse]


class StateResponse(BaseSchema):
    """
    Response schema for state details.
    """

    id: UUID
    name: str
    country: str


class ListStatesResponse(BaseSchema):
    """
    Response schema for listing states.
    """

    records: list[StateResponse]


class GetUniversityResponse(BaseSchema):
    """
    Response schema for getting university details.
    """

    id: UUID
    name: str
    location: str
    image: str
    state: str
    description: str | None
    acceptance_rate: str
    annual_fee: str
    student_faculty_ratio: str | None
    available_majors: list[UniversityMajorResponse]
    admission_requirements: list[str]
    degree: list[UniversityDegreeResponse]
    url: str
    rating: float


class ListUniversitiesResponse(PaginatedSchema):
    """
    Response schema for listing universities.
    """

    records: list[GetUniversityResponse]


class GetAdminUniversityResponse(BaseSchema):
    """
    Response schema for getting university details.
    """

    id: UUID
    name: str
    location: str
    image: str
    state: str
    description: str | None
    acceptance_rate: str
    annual_fee: str
    student_faculty_ratio: str | None
    available_majors: list[UniversityMajorResponse]
    admission_requirements: list[str]
    view_count: int
    status: UniversityStatus
    degree: list[UniversityDegreeResponse]
    url: str
    rating: float
    featured: bool


class ListAdminUniversitiesResponse(PaginatedSchema):
    """
    Response schema for listing universities.
    """

    records: list[GetAdminUniversityResponse]
