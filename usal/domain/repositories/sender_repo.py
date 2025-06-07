from abc import ABC, abstractmethod
from uuid import UUID


class SenderRepo(ABC):
    @abstractmethod
    async def send_otp(
        self,
        message_to: str,
        otp: str,
        name: str,
    ) -> None:
        """
        Send an OTP (One-Time Password) to a user for verification.

        Parameters:
        - `otp_type` (OTPType): The type of OTP.
        - `otp` (str): The OTP (One-Time Password) to be sent.
        - `name` (str): The name of the user who will receive the OTP.
        """

    @abstractmethod
    async def resend_link(
        self,
        verification_id: UUID,
        otp: str,
        name: str,
        email: str,
    ) -> None:
        """
        Resend the verification link to a user for verification.

        Args:
        - `verification_id` (UUID): The unique identifier of the verification.
        - `otp` (str): The OTP (One-Time Password) to be sent.
        - `name` (str): The name of the user or organization who will receive the OTP.
        - `org_name` (str): The name of the organization.
        """
