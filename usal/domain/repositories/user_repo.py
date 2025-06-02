from abc import abstractmethod
from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.domain.entities.user_entity import GetUserEntity, VerifyUserEntity


class UserRepo(DbRepo):
    @abstractmethod
    async def user_create(
        self,
        full_name: str,
        email: str,
        phone_number: str,
        password: str,
    ) -> VerifyUserEntity:
        """
        Create a new user.

        Parameters:
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            email (str): Email address of the user.
            phone_number (str): Phone number of the user.
            password (str): Password for the user account.
            middle_name (str | None): Middle name of the user, optional.

        Returns:
            None
        """

    @abstractmethod
    async def user_exists(
        self,
        email: str,
    ) -> bool:
        """
        Check if a user exists by email or phone number.

        Parameters:
            email (str): Email address of the user.
            phone_number (str): Phone number of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
    ) -> VerifyUserEntity:
        """
        Get a user by email.

        Parameters:
            email (str): Email address of the user.

        Returns:
            VerifyUserEntity: The user entity if found, otherwise raises an exception.
        """

    @abstractmethod
    async def verify_user(self, user_id: UUID) -> None:
        """
        Update a user's verification status to mark them as verified.

        Args:
            user_id (str): The unique user identifier to mark as verified.
        """

    @abstractmethod
    async def update_password(
        self,
        user_id: UUID,
        new_password: str,
    ) -> None:
        """
        Update a user's password.

        Parameters:
            user_id (UUID): The unique identifier of the user.
            new_password (str): The new password to set for the user.

        Returns:
            None
        """

    @abstractmethod
    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> GetUserEntity:
        """
        Get a user by their unique identifier.

        Parameters:
            user_id (UUID): The unique identifier of the user.

        Returns:
            GetUserEntity: The user entity if found, otherwise raises an exception.
        """
