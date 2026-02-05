import os

import boto3

from config_file import AWS_ENDPOINT_URL, AWS_REGION, S3_BUCKET


class S3Service:
    def __init__(self):
        self.endpoint_url = os.getenv("AWS_ENDPOINT_URL")
        self.public_endpoint_url = os.getenv("LOCALSTACK_PUBLIC_URL", "http://localhost:4566")
        self.client = boto3.client(
            "s3",
            region_name=AWS_REGION,
            endpoint_url=self.endpoint_url
        )

    # -------------------------
    # Upload URL
    # -------------------------
    def generate_upload_url(
        self,
        s3_key: str,
        content_type: str,
        expires_in: int = 900
    ) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": S3_BUCKET,
                "Key": s3_key,
                "ContentType": content_type
            },
            ExpiresIn=expires_in
        ).replace(self.endpoint_url, self.public_endpoint_url)

    # -------------------------
    # Download URL
    # -------------------------
    def generate_download_url(
        self,
        s3_key: str,
        expires_in: int = 900
    ) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": S3_BUCKET,
                "Key": s3_key
            },
            ExpiresIn=expires_in
        ).replace(self.endpoint_url, self.public_endpoint_url)

    # -------------------------
    # Delete Object
    # -------------------------
    def delete_object(self, s3_key: str):
        self.client.delete_object(
            Bucket=S3_BUCKET,
            Key=s3_key
        )
