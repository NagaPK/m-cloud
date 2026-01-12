from services.image_service import ImageService

service = ImageService()

# Create image
result = service.create_image(
    owner_id="test123",
    content_type="text/plain",
    size_bytes=12,
    tags=["docs", "test"]
)

print("Create result:", result)

image_id = result["image_id"]

# Upload file
import requests
requests.put(
    result["upload_url"],
    data=b"hello service layer",
    headers={"Content-Type": "text/plain"}
)

# Get download URL
download = service.get_image_download_url(image_id)
print("Download URL:", download)

# Download content
print(requests.get(download["download_url"]).text)

# List by owner
print("List by owner:", service.list_images(owner_id="test123"))

# Delete image
service.delete_image(image_id)
print("Image deleted")
