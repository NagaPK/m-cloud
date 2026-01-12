from repositories.image_repository import ImageRepository
from models.image import Image

repo = ImageRepository()

image = Image.create(
    owner_id="test123",
    content_type="image/png",
    size_bytes=12345,
    tags=["profile", "avatar"]
)

repo.create_image(image)

print("Image saved:", image.image_id)

item = repo.get_image(image.image_id)
print("Fetched image:", item)

print("List by owner:")
print(repo.list_by_owner("test123"))

print("List by tag:")
print(repo.list_by_tag("profile"))
