import boto3
from pathlib import Path
from src.constants import S3_BUCKET_NAME

s3 = boto3.client("s3")


def upload_file_to_s3(local_path: Path, s3_key: str):
    s3.upload_file(
        Filename=str(local_path),
        Bucket=S3_BUCKET_NAME,
        Key=s3_key
    )


def download_file_from_s3(local_path: Path, s3_key: str):
    local_path.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
        Filename=str(local_path)
    )
