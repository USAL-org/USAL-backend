from uuid import UUID
from pydantic import Field
from usal.api.schema.request.common_request import PaginationRequest
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
    acceptance_rate: float = Field(description="Acceptance rate of the university")
    annual_fee: float = Field(description="Annual fee of the university")
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
    rating: float = Field(description="Rating of the university")
    url: str = Field(description="URL of the university's official website")
    featured: bool = Field(
        default=False, description="Whether the university is featured or not"
    )
    degrees: list[UUID] = Field(
        description="List of degree IDs associated with the university"
    )
    test_required: bool = Field(
        default=False, description="Whether a test is required for admission"
    )
    min_gpa: float = Field(
        le=4.0,
        gt=0.0,
        description="Minimum GPA required for admission to the university",
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
    acceptance_rate: float | None = Field(
        None, description="Acceptance rate of the university"
    )
    annual_fee: float | None = Field(None, description="Annual fee of the university")
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


class MajorAndStateFilterRequest(BaseRequest):
    """
    Request model for filtering universities by major and state.
    """

    search: str | None = Field(
        None, description="Search term for filtering universities"
    )


class AdminUniversityFilterRequest(PaginationRequest):
    """
    Request model for filtering universities in admin panel.
    """

    search: str | None = Field(
        None, description="Search term for filtering universities"
    )


class UniversityFilterRequest(PaginationRequest):
    """
    Request model for filtering universities.
    """

    search: str | None = Field(
        None, description="Search term for filtering universities"
    )
    state: UUID | None = Field(
        None, description="State ID where the university is located"
    )
    major: UUID | None = Field(None, description="Major ID for filtering universities")
    application_fee: bool | None = Field(
        None, description="Whether to filter universities with an application fee"
    )
    community_college: bool | None = Field(
        None, description="Whether to filter community colleges"
    )
    degree: UUID | None = Field(
        None, description="Degree ID for filtering universities"
    )


class MatchUniversityRequest(PaginationRequest):
    """
    Request model for matching universities based on user preferences.
    """

    major: UUID = Field(description="Major ID for filtering universities")
    degree: UUID = Field(description="Degree ID for filtering universities")
    min_gpa: float = Field(
        le=4.0,
        gt=0.0,
        description="Minimum GPA required for admission to the university",
    )
    test_required: bool = Field(description="Whether a test is required for admission")
    min_fee: float = Field(description="Minimum annual fee of the university")
    max_fee: float = Field(description="Maximum annual fee of the university")


class StateRequest(BaseRequest):
    """
    Request model for getting universities by state.
    """

    name: str = Field(description="Name of the state")
    country: str = Field(description="Country of the state")
