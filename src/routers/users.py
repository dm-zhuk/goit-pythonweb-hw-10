import logging

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    UploadFile,
    BackgroundTasks,
    Depends,
    File,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from typing import Optional

from src.database.connect import get_db
from src.schemas.schemas import UserCreate, UserResponse, Token, RequestEmail
from src.services.email import send_verification_email
from src.services.auth import auth_service
from src.services.base import settings
from src.services.get_upload import get_upload_file_service
from src.services.redis import get_r_client
from src.repository.users import create_user, get_user_by_email, confirm_email


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["users"])
upload_service = get_upload_file_service()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    r: redis.Redis = Depends(get_r_client),
):
    db_user = await create_user(user, db, r)
    token = await auth_service.create_email_token({"sub": db_user.email})
    background_tasks.add_task(
        send_verification_email, db_user.email, token, str(settings.BASE_URL)
    )
    return db_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    r: redis.Redis = Depends(get_r_client),
):
    email = form_data.username
    user = await get_user_by_email(email, db, r)

    if not user or not auth_service.verify_password(
        form_data.password, user.hashed_password
    ):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await auth_service.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db),
    r: redis.Redis = Depends(get_r_client),
):
    email = await auth_service.get_email_from_token(token)
    user = await get_user_by_email(email, db, r)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.is_verified:
        return {"message": "Email already verified"}

    await confirm_email(email, db, r)
    return {"message": "Email verified successfully"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    r: Optional[redis.Redis] = Depends(get_r_client),
):
    user = await get_user_by_email(body.email, db, r)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
        )

    token = await auth_service.create_email_token({"sub": user.email})
    background_tasks.add_task(
        send_verification_email, body.email, token, str(settings.BASE_URL)
    )
    return {"message": "Verification email sent successfully"}


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def read_users_me(
    current_user: UserResponse = Depends(auth_service.get_current_user),
):
    return current_user


@router.patch("/me/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(),
    current_user: UserResponse = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
    r: Optional[redis.Redis] = Depends(get_r_client),
):
    try:
        image_url = upload_service.upload_file(file, current_user.email)
    except Exception as e:
        logger.error(f"Failed to upload avatar: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload avatar",
        )

    user = await get_user_by_email(current_user.email, db, r)
    user.avatar_url = image_url
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return UserResponse.model_validate(user)
