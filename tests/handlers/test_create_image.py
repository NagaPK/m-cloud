from handlers.create_image import handler
import json

def test_create_image_handler_success(mocker):
    mocker.patch(
        "handlers.create_image.ImageService.create_image",
        return_value={"image_id": "123", "upload_url": "url"}
    )

    event = {
        "body": json.dumps({
            "owner_id": "test123",
            "content_type": "image/png",
            "size_bytes": 10
        })
    }

    response = handler(event, None)

    assert response["statusCode"] == 201
