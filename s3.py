import argparse
import os
import pathlib
import boto3
import filetype
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--dir", required=True, choices=["category", "group", "part"])
args = parser.parse_args()

load_dotenv()

BASE_DIR = pathlib.Path(f"image/{args.dir}")
BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def upload_file(file_path: pathlib.Path):
    guess = filetype.guess(file_path.as_posix())
    content_type = guess.mime if guess else "application/octet-stream"

    s3_key = f"{args.dir}/{file_path.name}"
    print(f"uploading {file_path} -> s3://{BUCKET}/{s3_key}")

    s3.upload_file(
        Filename=str(file_path),
        Bucket=BUCKET,
        Key=s3_key,
        ExtraArgs={
            "ContentType": content_type,
            "CacheControl": "public, max-age=31536000, immutable"
        }
    )


def main():
    print(BASE_DIR)
    for file in BASE_DIR.rglob("*"):
        if file.name == '.gitkeep' or not file.suffix:
            continue
        upload_file(file)


if __name__ == "__main__":
    main()
