from abc import abstractmethod
from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.core.enums.university import UniversityStatus
from usal.domain.entities.university_entity import (
    ListAdminUniversitiesEntity,
    ListStatesEntity,
    ListUniversitiesEntity,
    ListUniversityMajorsEntity,
)


class UniversityRepo(DbRepo):
    @abstractmethod
    async def list_states(
        self,
        search: str | None = None,
    ) -> ListStatesEntity:
        """
        List all states.

        Returns:
            ListStatesEntity: List of states.
        """

    @abstractmethod
    async def add_university_major(
        self,
        name: str,
    ) -> None:
        """
        Add a university major.

        Parameters:
            name (str): Name of the university major.
            description (str | None): Description of the university major.

        Returns:
            None
        """

    @abstractmethod
    async def list_university_majors(
        self,
        search: str | None = None,
    ) -> ListUniversityMajorsEntity:
        """
        List all university majors.

        Returns:
            ListUniversityMajorsEntity: List of university majors.
        """

    @abstractmethod
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
        """
        Add a university.

        Parameters:
            name (str): Name of the university.
            location (str): Location of the university.
            image (str): Image URL of the university.
            application_fee (float): Application fee of the university.
            community_college (bool): Whether the university is a community college.
            state (UUID): State ID where the university is located.
            description (str): Description of the university.
            acceptance_rate (str): Acceptance rate of the university.
            annual_fee (str): Annual fee of the university.
            student_faculty_ratio (str): Student to faculty ratio of the university.
            available_majors (list[UUID]): List of available majors in the university.
            admission_requirements (list[str]): List of admission requirements for the university.
            status (UniversityStatus): Status of the university.

        Returns:
            None
        """

    @abstractmethod
    async def list_universities(
        self,
        page: int,
        limit: int,
        search: str | None = None,
    ) -> ListAdminUniversitiesEntity:
        """
        List all universities.

        Parameters:
            page (int): Page number for pagination.
            limit (int): Number of records per page.
            search (str | None): Search term for filtering universities.

        Returns:
            ListUniversitiesEntity: List of universities.
        """

    @abstractmethod
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
        """
        List all universities.

        Parameters:
            page (int): Page number for pagination.
            limit (int): Number of records per page.
            search (str | None): Search term for filtering universities.
            state (UUID | None): State ID for filtering universities.
            major (UUID | None): Major ID for filtering universities.
            application_fee (bool | None): Filter by application fee.
            community_college (bool | None): Filter by community college status.

        Returns:
            ListUniversitiesEntity: List of universities.
        """
