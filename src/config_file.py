import os

AWS_REGION = "us-east-1"
DYNAMODB_TABLE = "Images"
S3_BUCKET = "image-bucket"

IS_LOCAL = os.getenv("IS_LOCAL", "true") == "true"

AWS_ENDPOINT_URL = "http://localhost:4566" if IS_LOCAL else None