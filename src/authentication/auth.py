# src/authentication/auth.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import aiosmtplib
from email.message import EmailMessage
from src.settings.base import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_verification_token(email: str):
    data = {"sub": email, "type": "verify"}
    return create_access_token(data)


async def send_verification_email(email: str, token: str):
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = email
    message["Subject"] = "Verify Your Email"
    verification_link = f"http://localhost:8000/users/verify?token={token}"
    message.set_content(
        f"Please verify your email by clicking this link: {verification_link}"
    )
    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
        use_tls=True,
    )
