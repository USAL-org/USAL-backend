import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import override
from uuid import UUID

from aiosmtplib import send

from usal.core.config import EmailConfig
from usal.domain.repositories.sender_repo import SenderRepo
from usal.util.template import render_template


class DbSenderRepo(SenderRepo):
    def __init__(self) -> None:
        self.config = EmailConfig.build()

    async def _send(self, message_to: str, subject: str, msg: str) -> None:
        message = MIMEMultipart("alternative")
        message["From"] = self.config.username
        message["To"] = message_to
        message["Subject"] = subject
        message.attach(MIMEText(msg, "html"))

        try:
            await send(
                message,
                hostname=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
            )

        except Exception as e:
            logging.error("Error occurred while sending email:", e)

    @override
    async def send_otp(
        self,
        message_to: str,
        otp: str,
        name: str,
    ) -> None:
        html_message = render_template(
            template_path="usal/templates/emails/email-verify.html",
            data={"otp": otp, "name": name},
        )
        await self._send(message_to, subject="OTP Verification", msg=html_message)

    @override
    async def resend_link(
        self,
        verification_id: UUID,
        otp: str,
        name: str,
        email: str,
    ) -> None:
        html_message = render_template(
            template_path="himalaya/templates/emails/resend-link.html",
            data={
                "name": name,
                "link": f"hms.hridayangam.tech/v1/staff/verify?verification_id={verification_id}&otp={otp}",
            },
        )

        await self._send(
            message_to=email,
            subject="Resending Staff Verification Link Request",
            msg=html_message,
        )
