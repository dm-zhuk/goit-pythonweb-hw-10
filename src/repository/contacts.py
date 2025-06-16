from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, extract, func
from datetime import date, timedelta

from src.database.models import Contact, User
from src.schemas.schemas import ContactCreate, ContactUpdate


async def create_contact(db: AsyncSession, contact: ContactCreate, user: User):
    db_contact = Contact(**contact.model_dump(), user_id=user.id)
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact


async def get_contacts(db: AsyncSession, user: User, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_contact(db: AsyncSession, contact_id: int, user: User):
    result = await db.execute(
        select(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id)
    )
    return result.scalars().first()


async def update_contact(
    db: AsyncSession, contact_id: int, contact: ContactUpdate, user: User
):
    result = await db.execute(
        select(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id)
    )
    db_contact = result.scalars().first()
    if db_contact:
        for key, value in contact.model_dump(exclude_unset=True).items():
            setattr(db_contact, key, value)
        await db.commit()
        await db.refresh(db_contact)
        return db_contact
    return None


async def delete_contact(db: AsyncSession, contact_id: int, user: User):
    result = await db.execute(
        select(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id)
    )
    db_contact = result.scalars().first()
    if db_contact:
        await db.delete(db_contact)
        await db.commit()
    return db_contact


async def search_contacts(db: AsyncSession, query: str, user: User):
    result = await db.execute(
        select(Contact).filter(
            Contact.user_id == user.id,
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            ),
        )
    )
    return result.scalars().all()


async def get_upcoming_birthdays(
    db: AsyncSession, user: User, days: int = 7, start_date: date = None
):
    if days < 1:
        raise HTTPException(status_code=400, detail="Days must be positive")
    start = start_date or date.today()
    end = start + timedelta(days=days)
    result = await db.execute(
        select(
            Contact.id,
            Contact.first_name,
            Contact.last_name,
            func.to_char(Contact.birthday, "MON-DD").label("birthday_formatted"),
        ).filter(
            Contact.user_id == user.id,
            or_(
                (extract("month", Contact.birthday) == extract("month", start))
                & (
                    extract("day", Contact.birthday).between(
                        extract("day", start), extract("day", end)
                    )
                ),
                (extract("month", Contact.birthday) == extract("month", end))
                & (extract("day", Contact.birthday) <= extract("day", end)),
            ),
        )
    )
    contacts = result.all()
    return [
        {
            "message": f"{contact.first_name} {contact.last_name}'s birthday is on {contact.birthday_formatted} (ID: {contact.id})"
        }
        for contact in contacts
    ]
