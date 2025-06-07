from uuid import UUID

from usal.core import BaseEntity
from usal.domain.entities.common_entity import PageEntity


class UniversityMajorEntity(BaseEntity):
    """
    Entity model for university majors.
    """

    id: UUID
    name: str


class ListUniversityMajorsEntity(BaseEntity):
    """
    Entity model for listing university majors.
    """

    records: list[UniversityMajorEntity]


class StateEntity(BaseEntity):
    """
    Entity model for state details.
    """

    id: UUID
    name: str
    country: str


class ListStatesEntity(BaseEntity):
    """
    Entity model for listing states.
    """

    records: list[StateEntity]


class GetUniversityEntity(BaseEntity):
    """
    Entity model for getting university details.
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
    available_majors: list[UniversityMajorEntity]
    admission_requirements: list[str]


class ListUniversitiesEntity(BaseEntity):
    """
    Entity model for listing universities.
    """

    page_info: PageEntity
    records: list[GetUniversityEntity]


class GetAdminUniversityEntity(BaseEntity):
    """
    Entity model for getting university details.
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
    available_majors: list[UniversityMajorEntity]
    admission_requirements: list[str]
    view_count: int
    status: str


class ListAdminUniversitiesEntity(BaseEntity):
    """
    Entity model for listing universities.
    """

    page_info: PageEntity
    records: list[GetAdminUniversityEntity]
