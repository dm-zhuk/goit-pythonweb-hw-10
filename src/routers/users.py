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

from src.database.connect import get_db
from src.schemas.schemas import UserCreate, UserResponse, Token, RequestEmail
from src.repository.users import create_user, get_user_by_email, confirm_email
from src.services.email import send_verification_email
from src.settings.auth import auth_service
from src.settings.base import settings
from src.settings.cloudinary_config import cloudinary

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    try:
        db_user = await create_user(user, db, auth_service)
        token = auth_service.create_email_token({"sub": db_user.email})
        background_tasks.add_task(
            send_verification_email, db_user.email, token, str(settings.BASE_URL)
        )

        return db_user

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await get_user_by_email(form_data.username, db)
    if not user or not auth_service.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = auth_service.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.is_verified:
        return {"message": "Email already verified"}
    await confirm_email(email, db)
    return {"message": "Email verified successfully"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await get_user_by_email(body.email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified"
            )

        token = auth_service.create_email_token({"sub": user.email})
        background_tasks.add_task(
            send_verification_email, user.email, token, str(settings.BASE_URL)
        )

        return {"message": "Verification email sent successfully"}

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def read_users_me(
    current_user: UserResponse = Depends(auth_service.get_current_user),
):
    return current_user


@router.post("/me/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        upload_result = cloudinary.uploader.upload(file.file, folder="avatars")
        image_url = upload_result["secure_url"]
        current_user.avatar_url = image_url
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)

        return current_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
