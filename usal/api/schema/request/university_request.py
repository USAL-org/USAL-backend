from uuid import UUID
from pydantic import Field
from usal.core import BaseRequest
from usal.core.enums.university import UniversityStatus


class AddUniversityRequest(BaseRequest):
    """
    Request model for adding a university.
    """

    name: str = Field(description="Name of the university")
    location: str = Field(description="Location of the university")
    image: str = Field(description="Image URL of the university")
    application_fee: bool = Field(
        description="Whether the university has an application fee"
    )
    community_college: bool = Field(
        description="Whether the university is a community college"
    )
    state: UUID = Field(description="State ID where the university is located")
    description: str = Field(description="Description of the university")
    acceptance_rate: str = Field(description="Acceptance rate of the university")
    annual_fee: str = Field(description="Annual fee of the university")
    student_faculty_ratio: str = Field(
        description="Student to faculty ratio of the university"
    )
    available_majors: list[UUID] = Field(
        description="List of available majors in the university"
    )
    admission_requirements: list[str] = Field(
        description="List of admission requirements for the university"
    )
    status: UniversityStatus = Field(
        description="Status of the university (e.g., active, inactive)"
    )


class UpdateUniversityRequest(BaseRequest):
    """
    Request model for updating a university.
    """

    name: str | None = Field(None, description="Name of the university")
    location: str | None = Field(None, description="Location of the university")
    image: str | None = Field(None, description="Image URL of the university")
    application_fee: bool | None = Field(
        None, description="Whether the university has an application fee"
    )
    community_college: bool | None = Field(
        None, description="Whether the university is a community college"
    )
    state: UUID | None = Field(
        None, description="State ID where the university is located"
    )
    description: str | None = Field(None, description="Description of the university")
    acceptance_rate: str | None = Field(
        None, description="Acceptance rate of the university"
    )
    annual_fee: str | None = Field(None, description="Annual fee of the university")
    student_faculty_ratio: str | None = Field(
        None, description="Student to faculty ratio of the university"
    )
    available_majors: list[UUID] | None = Field(
        None, description="List of available majors in the university"
    )
    admission_requirements: list[str] | None = Field(
        None, description="List of admission requirements for the university"
    )
    status: UniversityStatus | None = Field(
        None, description="Status of the university (e.g., active, inactive)"
    )


class AddUniversityMajorRequest(BaseRequest):
    """
    Request model for adding a university major.
    """

    name: str = Field(description="Name of the university major")


class UpdateUniversityMajorRequest(BaseRequest):
    """
    Request model for updating a university major.
    """

    name: str | None = Field(None, description="Name of the university major")
