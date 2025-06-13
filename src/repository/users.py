from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.database.models import User
from src.schemas.schemas import UserCreate


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(User.__table__.select().where(User.email == email))
    return result.scalars().first()


async def create_user(body: UserCreate, db: AsyncSession, auth_service) -> User:
    existing_user = await get_user_by_email(body.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    hashed_password = auth_service.get_password_hash(body.password)
    new_user = User(email=body.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def confirm_email(email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if user:
        user.is_verified = True
        await db.commit()
