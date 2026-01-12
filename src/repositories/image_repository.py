import boto3
from typing import List, Optional
from config_file import AWS_ENDPOINT_URL, AWS_REGION, DYNAMODB_TABLE
from models.image import Image


class ImageRepository:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
            endpoint_url=AWS_ENDPOINT_URL
        )
        self.table = self.dynamodb.Table(DYNAMODB_TABLE)

    # Create
    def create_image(self, image: Image):
        item = {
            "PK": f"IMAGE#{image.image_id}",
            "SK": "METADATA",

            "image_id": image.image_id,
            "owner_id": image.owner_id,
            "s3_key": image.s3_key,
            "content_type": image.content_type,
            "size_bytes": image.size_bytes,
            "tags": image.tags,
            "created_at": image.created_at,

            "GSI1PK": f"OWNER#{image.owner_id}",
            "GSI1SK": image.created_at,
        }

        self.table.put_item(Item=item)

        # create one item per tag for GSI2
        for tag in image.tags:
            self.table.put_item(
                Item={
                    "PK": f"IMAGE#{image.image_id}",
                    "SK": f"TAG#{tag}",
                    "GSI2PK": f"TAG#{tag}",
                    "GSI2SK": image.created_at,
                }
            )

    # Get by ID
    def get_image(self, image_id: str) -> Optional[dict]:
        response = self.table.get_item(
            Key={
                "PK": f"IMAGE#{image_id}",
                "SK": "METADATA"
            }
        )
        return response.get("Item")

    # List by owner
    def list_by_owner(self, owner_id: str, limit: int = 20):
        response = self.table.query(
            IndexName="GSI1",
            KeyConditionExpression="GSI1PK = :pk",
            ExpressionAttributeValues={
                ":pk": f"OWNER#{owner_id}"
            },
            Limit=limit
        )
        return response.get("Items", [])

    # List by tag
    def list_by_tag(self, tag: str, limit: int = 20):
        response = self.table.query(
            IndexName="GSI2",
            KeyConditionExpression="GSI2PK = :pk",
            ExpressionAttributeValues={
                ":pk": f"TAG#{tag}"
            },
            Limit=limit
        )
        return response.get("Items", [])
