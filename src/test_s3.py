from services.s3_service import S3Service

s3 = S3Service()

key = "images/test-image.txt"

upload_url = s3.generate_upload_url(
    s3_key=key,
    content_type="text/plain"
)

download_url = s3.generate_download_url(key)

print("UPLOAD URL:")
print(upload_url)

print("\nDOWNLOAD URL:")
print(download_url)
