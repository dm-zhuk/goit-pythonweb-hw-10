from src.services.cloudinary_config import UploadFileService
from src.services.base import settings


def get_upload_file_service() -> UploadFileService:
    return UploadFileService(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )
