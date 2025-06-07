"""Define functions for CRUD operations (to interact with DB) and search/birthday logic"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import extract, func
from src.database.models import Contact
from src.schemas.contact import ContactCreate, ContactUpdate
from datetime import date, timedelta


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        try:
            for key, value in contact.model_dump(exclude_unset=True).items():
                setattr(db_contact, key, value)
            db.commit()
            db.refresh(db_contact)
            return db_contact
        except (IntegrityError, DataError) as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")
    return None


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, query: str):
    return (
        db.query(Contact)
        .filter(
            (Contact.first_name.ilike(f"%{query}%"))
            | (Contact.last_name.ilike(f"%{query}%"))
            | (Contact.email.ilike(f"%{query}%"))
        )
        .all()
    )


def get_upcoming_birthdays(db: Session, days: int = 7, start_date: date = None):
    if days < 1:
        raise HTTPException(status_code=400, detail="Days must be positive")

    start = start_date or date.today()
    end = start + timedelta(days=days)

    contacts = (
        db.query(
            Contact.id,
            Contact.first_name,
            Contact.last_name,
            func.to_char(Contact.birthday, "MON-DD").label("birthday_formatted"),
        )
        .filter(
            (
                (extract("month", Contact.birthday) == extract("month", start))
                & (
                    extract("day", Contact.birthday).between(
                        extract("day", start), extract("day", end)
                    )
                )
            )
            | (
                (extract("month", Contact.birthday) == extract("month", end))
                & (extract("day", Contact.birthday) <= extract("day", end))
            )
        )
        .all()
    )

    return [
        {
            "message": f"{contact.first_name} {contact.last_name}'s birthday is on {contact.birthday_formatted} (ID: {contact.id})"
        }
        for contact in contacts
    ]
