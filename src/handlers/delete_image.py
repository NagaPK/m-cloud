import json
from services.image_service import ImageService


def handler(event, context):
    image_id = event["pathParameters"]["image_id"]

    service = ImageService()

    try:
        service.delete_image(image_id)
    except ValueError as e:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": str(e)})
        }

    return {
        "statusCode": 204,
        "body": ""
    }
