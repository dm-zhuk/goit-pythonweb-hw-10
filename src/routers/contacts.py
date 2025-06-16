from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from src.database.connect import get_db
from src.schemas.schemas import (
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
from src.database.models import User
from datetime import date
from src.services.auth import auth_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_new_contact(
    contact: ContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    try:
        return await create_contact(db, contact, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    try:
        return await get_contacts(db, current_user, skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    try:
        contact = await get_contact(db, contact_id, current_user)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
            )
        return contact
    except HTTPException as e:
        raise e  # Re-raise known HTTP exceptions
    except Exception as e:
        logger.error(f"Error retrieving contact: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts_by_query(
    query: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    try:
        return await search_contacts(db, query, current_user)
    except Exception as e:
        logger.error(f"Error searching contacts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_existing_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    updated_contact = await update_contact(db, contact_id, contact, current_user)
    if not updated_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await delete_contact(db, contact_id, current_user)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return None


@router.get("/birthdays/", response_model=List[BirthdayResponse])
async def get_contacts_with_upcoming_birthdays(
    days: int = 7,
    start_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    try:
        return await get_upcoming_birthdays(db, current_user, days, start_date)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
