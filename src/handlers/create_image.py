import json
import os

from config_file import AWS_ENDPOINT_URL
from services.image_service import ImageService


def handler(event, context):
    body = json.loads(event.get("body", "{}"))

    owner_id = body.get("owner_id")
    content_type = body.get("content_type")
    size_bytes = body.get("size_bytes")
    tags = body.get("tags", [])

    if not AWS_ENDPOINT_URL:
        raise RuntimeError("AWS_ENDPOINT_URL is not set - Lambda cannot reach AWS Services")

    print("AWS_ENDPOINT_URL =", os.getenv("AWS_ENDPOINT_URL"))

    if not owner_id or not content_type or not size_bytes:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required fields"})
        }

    service = ImageService()
    result = service.create_image(
        owner_id=owner_id,
        content_type=content_type,
        size_bytes=size_bytes,
        tags=tags
    )

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
