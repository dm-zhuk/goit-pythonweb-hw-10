from pydantic import EmailStr
from pydantic.fields import Field

from src.schemas.schema import BaseSchema


class SignUpSchema(BaseSchema):
    """Schema for sign up validation."""

    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6, max_length=50)


class RequestEmail(BaseSchema):
    """Schema for requesting email validation."""

    email: EmailStr


class InfoSchema(BaseSchema):
    """Schema for sign up success response."""

    message: str


class LoginSchema(BaseSchema):
    """Schema for login validation."""

    email: EmailStr
    password: str = Field(min_length=6, max_length=50)


class LoginSuccessSchema(BaseSchema):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    access_token: str


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str = "bearer"  # noqa: S105
