"""Data Validation with Pydantic - ensures data sent to API is valid"""

from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    birthday: date
    additional_data: Optional[str] = None

    class ConfigDict:
        from_attributes = True


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    birthday: Optional[date] = None


class ContactResponse(ContactBase):
    id: int


class BirthdayResponse(BaseModel):
    message: str
