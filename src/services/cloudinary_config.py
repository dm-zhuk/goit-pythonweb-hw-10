import cloudinary
import cloudinary.uploader
from fastapi import UploadFile


class UploadFileService:
    def __init__(self, cloud_name, api_key, api_secret):
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

    def upload_file(self, file: UploadFile, username: str) -> str:
        public_id = f"RestApp/{username}"
        try:
            r = cloudinary.uploader.upload(
                file.file, public_id=public_id, overwrite=True
            )
            src_url = cloudinary.CloudinaryImage(public_id).build_url(
                width=250, height=250, crop="fill", version=r.get("version")
            )
            return src_url
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
