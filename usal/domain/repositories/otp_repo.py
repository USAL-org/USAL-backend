from abc import abstractmethod
from datetime import datetime
from uuid import UUID

from usal.core.db_repo import DbRepo
from usal.domain.entities.user_entity import OTPEntity


class OTPRepo(DbRepo):
    @abstractmethod
    async def generate_otp(
        self,
        secret: str,
        expiration_time: datetime,
        user_id: UUID,
    ) -> OTPEntity:
        """
        Create or update an OTP for a user.

        Args:
            secret (str): The OTP secret.
            expiration_time (datetime): The expiration time of the OTP.
            user_id (UUID): The unique identifier of the user.

        Returns:
            OTPEntity: The created or updated OTP entity.
        """

    @abstractmethod
    async def get_otp(self, verification_id: UUID) -> OTPEntity:
        """
        Retrieve a user's OTP by verification ID.

        Args:
            verification_id (str): The verification ID of the OTP.

        Returns:
            OTPEntity: The OTP entity.
        """

    @abstractmethod
    async def save_and_send(
        self,
        name: str,
        user_id: UUID,
        email: str | None = None,
        resend: bool | None = False,
    ) -> OTPEntity:
        """
        Save and send an OTP to the user.

        Args:
        - `name` (str): The name of the user.
        - `user_id` (UUID): The unique identifier of the user.
        - `email` (str | None): The email address of the user (optional).
        - `resend` (bool | None): Whether to resend the OTP (default is False).

        Returns:
        - `OTPEntity`: The entity representing the saved OTP.
        """

    @abstractmethod
    async def verify(self, verification_id: UUID, secret: str) -> OTPEntity:
        """
        Verify the OTP for a user.

        Args:
            verification_id (UUID): The unique identifier of the OTP.
            secret (str): The OTP secret to verify.

        Returns:
            OTPEntity: The verified OTP entity.
        """
