import boto3
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def upload_file_to_s3(file, filename):
    try:
        # public 폴더 경로 설정
        key = f"public/{filename}"

        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        # S3 업로드 + 공개 권한 설정
        s3.upload_fileobj(
            Fileobj=file,
            Bucket=S3_BUCKET_NAME,
            Key=key,
            ExtraArgs={
                "ContentType": file.content_type,
                "ContentDisposition": "inline",
            },
        )

        # 퍼블릭 URL 구성
        url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
        return url

    except ClientError as e:
        raise ValueError(f"S3 Upload Error: {e}")


def delete_s3_file_by_url(file_url):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    parsed_url = urlparse(file_url)
    # 예: parsed_url.path = '/uploads/profile.jpg'
    key = parsed_url.path.lstrip("/")  # 앞에 '/' 제거

    s3.delete_object(Bucket=os.getenv("S3_BUCKET_NAME"), Key=key)
