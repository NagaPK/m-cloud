import json
from services.image_service import ImageService


def handler(event, context):
    params = event.get("queryStringParameters") or {}

    owner_id = params.get("owner_id")
    tag = params.get("tag")

    service = ImageService()

    try:
        images = service.list_images(
            owner_id=owner_id,
            tag=tag
        )
    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(images)
    }
