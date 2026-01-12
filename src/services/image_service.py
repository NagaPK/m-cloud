from typing import List, Optional, Dict
from repositories.image_repository import ImageRepository
from services.s3_service import S3Service
from models.image import Image


class ImageService:
    def __init__(self):
        self.repo = ImageRepository()
        self.s3 = S3Service()

    # -------------------------
    # Create image (metadata + upload URL)
    # -------------------------
    def create_image(
        self,
        owner_id: str,
        content_type: str,
        size_bytes: int,
        tags: List[str]
    ) -> Dict:
        image = Image.create(
            owner_id=owner_id,
            content_type=content_type,
            size_bytes=size_bytes,
            tags=tags
        )

        # Save metadata
        self.repo.create_image(image)

        # Generate upload URL
        upload_url = self.s3.generate_upload_url(
            s3_key=image.s3_key,
            content_type=content_type
        )

        return {
            "image_id": image.image_id,
            "upload_url": upload_url,
            "expires_in": 900
        }

    # -------------------------
    # List images (filter by owner or tag)
    # -------------------------
    def list_images(
        self,
        owner_id: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        if owner_id:
            return self.repo.list_by_owner(owner_id, limit)

        if tag:
            return self.repo.list_by_tag(tag, limit)

        raise ValueError("Either owner_id or tag must be provided")

    # -------------------------
    # Get image download URL
    # -------------------------
    def get_image_download_url(self, image_id: str) -> Dict:
        item = self.repo.get_image(image_id)

        if not item:
            raise ValueError("Image not found")

        download_url = self.s3.generate_download_url(
            s3_key=item["s3_key"]
        )

        return {
            "image_id": image_id,
            "download_url": download_url,
            "expires_in": 900
        }

    # -------------------------
    # Delete image (hard delete)
    # -------------------------
    def delete_image(self, image_id: str):
        item = self.repo.get_image(image_id)

        if not item:
            raise ValueError("Image not found")

        # Delete from S3
        self.s3.delete_object(item["s3_key"])

        # Delete metadata
        self.repo.table.delete_item(
            Key={
                "PK": f"IMAGE#{image_id}",
                "SK": "METADATA"
            }
        )
