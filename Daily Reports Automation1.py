import os
import zipfile
import boto3
from botocore.exceptions import ClientError

bucket_name = "daily-reports-backup-demo"
reports_folder = "daily_reports"
zip_filename = "daily_reports.zip"
region = "us-west-2"

s3 = boto3.client('s3', region_name=region)


def create_bucket_if_missing(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError:
        print(f"Bucket '{bucket_name}' not found. Creating...")
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region})
        
def create_dummy_reports(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")
    if not os.listdir(folder):
        for i in range(1, 4):
            file_path = os.path.join(folder, f"report_{i}.txt")
            with open(file_path, "w") as f:
                f.write(f"This is the content of report {i}.")
        print(f"Created dummy reports in {folder}")
    else:
        print(f"Reports already exist in {folder}")

def zip_reports(folder, zip_name):
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=filename)
    print(f"Created ZIP file: {zip_name}")

def upload_to_s3(file_name, bucket_name):
    try:
        s3.upload_file(file_name, bucket_name, file_name)
        print(f"Uploaded '{file_name}' to bucket '{bucket_name}'")
    except Exception as e:
        print(f"Failed to upload: {e}")

def main():
    create_bucket_if_missing(bucket_name)
    create_dummy_reports(reports_folder)
    zip_reports(reports_folder, zip_filename)
    upload_to_s3(zip_filename, bucket_name)

if __name__ == "__main__":
    main()
