from abc import abstractmethod
from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.core.enums.university import UniversityStatus
from usal.domain.entities.university_entity import (
    ListAdminUniversitiesEntity,
    ListStatesEntity,
    ListUniversitiesEntity,
    ListUniversityDegreesEntity,
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
    async def list_university_degrees(
        self,
    ) -> ListUniversityDegreesEntity:
        """
        List all university degrees.

        Returns:
            ListUniversityMajorsEntity: List of university degrees.
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
            degrees (list[UUID]): List of degree IDs associated with the university.
            rating (float): Rating of the university.
            url (str): URL of the university's official website.
            featured (bool): Whether the university is featured or not.


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
        degree: UUID | None = None,
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

    @abstractmethod
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
        """
        List featured universities.

        Parameters:
            page (int): Page number for pagination.
            limit (int): Number of records per page.
            search (str | None): Search term for filtering universities.
            state (UUID | None): State ID for filtering universities.
            major (UUID | None): Major ID for filtering universities.
            application_fee (bool | None): Filter by application fee.
            community_college (bool | None): Filter by community college status.

        Returns:
            ListUniversitiesEntity: List of featured universities.
        """

    @abstractmethod
    async def visit_university(
        self,
        university_id: UUID,
    ) -> None:
        """
        Increment the view count of a university.

        Parameters:
            university_id (UUID): ID of the university to visit.

        Returns:
            None
        """

    @abstractmethod
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
        """
        Match universities based on user preferences.

        Parameters:
            page (int): Page number for pagination.
            limit (int): Number of records per page.
            major (UUID): Major ID for filtering universities.
            degree (UUID): Degree ID for filtering universities.
            min_gpa (float): Minimum GPA required for admission.
            test_required (bool): Whether a test is required for admission.
            min_fee (float): Minimum annual fee of the university.
            max_fee (float): Maximum annual fee of the university.

        Returns:
            ListUniversitiesEntity: List of matched universities.
        """
