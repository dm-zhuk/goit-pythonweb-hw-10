import aiosmtplib

from email.message import EmailMessage

from src.settings.base import settings


async def send_verification_email(email: str, token: str):
    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = email
    message["Subject"] = "Verify Your Email"
    verification_link = f"http://127.0.0.1:8000/api/users/verify?token={token}"
    message.set_content(f"Please verify your email with this link: {verification_link}")
    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        use_tls=True,
    )
