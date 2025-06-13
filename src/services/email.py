from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pathlib import Path

from src.settings.base import settings

import logging

logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_SERVER,
    MAIL_FROM_NAME="Contacts Management API",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_verification_email(email: str, token: str, BASE_URL: str):
    try:
        message = MessageSchema(
            subject="Email Confirmation",
            recipients=[email],
            template_body={
                "host": BASE_URL,
                "username": email,
                "token": token,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
        logger.info(f"Verification email sent to {email}")
    except ConnectionErrors as e:
        logger.error(f"Failed to send verification email to {email}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending email to {email}: {e}")
        raise
