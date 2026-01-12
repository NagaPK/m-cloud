from dataclasses import dataclass
from typing import List
from datetime import datetime
import uuid


@dataclass
class Image:
    image_id: str
    owner_id: str
    s3_key: str
    content_type: str
    size_bytes: int
    tags: List[str]
    created_at: str

    @staticmethod
    def create(
            owner_id: str,
            content_type: str,
            size_bytes: int,
            tags: List[str]
    ) -> "Image":
        image_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        s3_key = f"images/{image_id}"

        return Image(
            image_id=image_id,
            owner_id=owner_id,
            s3_key=s3_key,
            content_type=content_type,
            size_bytes=size_bytes,
            tags=tags,
            created_at=created_at)
