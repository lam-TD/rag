import os, boto3
from botocore.config import Config

S3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    config=Config(signature_version="s3v4"),
)
BUCKET = os.getenv("MINIO_BUCKET", "docs")

def read_text_object(key: str) -> str:
    """Đọc file TXT từ MinIO (UTF-8)."""
    obj = S3.get_object(Bucket=BUCKET, Key=key)
    return obj["Body"].read().decode("utf-8", errors="ignore")
