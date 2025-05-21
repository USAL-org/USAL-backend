from uuid import UUID

from usal.core import BaseSchema


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
    available_majors: ListUniversityMajorsResponse
    admission_requirements: list[str]


class ListUniversitiesResponse(BaseSchema):
    """
    Response schema for listing universities.
    """

    records: list[GetUniversityResponse]
