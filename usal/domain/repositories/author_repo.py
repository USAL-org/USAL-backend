from abc import abstractmethod
# from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.domain.entities.author_entity import ListAuthorsEntity


class AuthorRepo(DbRepo):
    @abstractmethod
    async def create_author(
        self,
        full_name: str,
        email: str,
        short_description: str,
        pp_url: str | None = None,
        description: str | None = None,
        social_links: list[str] | None = None,
    ) -> None:
        """
        Create an author.

        Parameters:
            full_name (str): Name of the author.
            email (str): Email of the author.
            short_description (str): Short description of the author.
            pp_url (str | None): Profile picture URL of the author.
            description (str | None): Description of the author.
            social_links (list[str] | None): List of social links of the author.

        Returns:
            None
        """

    # @abstractmethod
    # async def update_author(
    #     self,
    #     author_id: UUID,
    #     full_name: str | None = None,
    #     email: str | None = None,
    #     short_description: str | None = None,
    #     pp_url: str | None = None,
    #     description: str | None = None,
    #     social_links: list[str] | None = None,
    # ) -> None:
    #     """
    #     Update an author.

    #     Parameters:
    #         author_id (UUID): ID of the author.
    #         full_name (str | None): Name of the author.
    #         email (str | None): Email of the author.
    #         short_description (str | None): Short description of the author.
    #         pp_url (str | None): Profile picture URL of the author.
    #         description (str | None): Description of the author.
    #         social_links (list[str] | None): List of social links of the author.

    #     Returns:
    #         None
    #     """

    @abstractmethod
    async def list_all_author(self) -> ListAuthorsEntity:
        """
        List all authors.

        Returns:
            ListAuthorsEntity: List of authors.
        """
