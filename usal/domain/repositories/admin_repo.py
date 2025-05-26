from abc import abstractmethod
from usal.core.db_repo import DbRepo
from usal.domain.entities.admin_entity import AdminEntity


class AdminRepo(DbRepo):
    @abstractmethod
    async def get_admin_by_username(self, username: str) -> AdminEntity:
        """
        Retrieve information about a specific admin by their username.

        Parameters:
            username (str): The username of the admin to be retrieved.

        Returns:
            AdminEntity: An instance of AdminEntity representing the admin with the
        specified username.
        """
