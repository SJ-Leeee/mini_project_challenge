import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def upload_file_to_s3(file, filename):
    try:
        key = f"public/{filename}"
        s3.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            key,
        )
        url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
        return url
    except ClientError as e:
        raise ValueError(f"S3 Upload Error: {e}")


def delete_file_from_s3(filename):
    try:
        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=filename)
        return True
    except ClientError as e:
        raise ValueError(f"S3 Delete Error: {e}")
