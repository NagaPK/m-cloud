import os

AWS_REGION = "us-east-1"
DYNAMODB_TABLE = "Images"
S3_BUCKET = "image-bucket"

AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")