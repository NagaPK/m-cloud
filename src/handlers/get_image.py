import json
from services.image_service import ImageService


def handler(event, context):
    image_id = event["pathParameters"]["image_id"]

    service = ImageService()

    try:
        result = service.get_image_download_url(image_id)
    except ValueError as e:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
