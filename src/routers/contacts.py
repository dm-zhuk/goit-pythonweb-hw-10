"""Defines the API endpoints (like /contacts) using FastAPI"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from src.database.connect import get_db
from src.schemas.contact import (
    ContactCreate,
    ContactResponse,
    ContactUpdate,
    BirthdayResponse,
)
from src.repository.contacts import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays,
)

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)


@router.get("/", response_model=list[ContactResponse])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_contacts(db, skip, limit)


@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_existing_contact(
    contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)
):
    updated_contact = update_contact(db, contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = delete_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None


@router.get("/search/", response_model=list[ContactResponse])
def search_contacts_by_query(query: str, db: Session = Depends(get_db)):
    return search_contacts(db, query)


@router.get("/birthdays/", response_model=List[BirthdayResponse])
def get_contacts_with_upcoming_birthdays(
    days: int = 7, start_date: Optional[date] = None, db: Session = Depends(get_db)
):
    return get_upcoming_birthdays(db, days=days, start_date=start_date)
