import json
from services.image_service import ImageService


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    last_key_param = params.get("last_key")

    owner_id = params.get("owner_id")
    tag = params.get("tag")

    service = ImageService()

    try:
        images = service.list_images(
            owner_id=owner_id,
            tag=tag,
            last_key=last_key_param
        )
        print(f"images result is {images}")
    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(images, default=str)
    }
