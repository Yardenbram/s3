import boto3
import os
from os.path import isfile, join

s3 = boto3.client('s3', region_name='us-west-2')
bucket_name = 'student-yarden-bra-backup'
folder_path = 'daily_documents'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    for i in range(1, 4):
        with open(f"{folder_path}/file{i}.txt", "w") as f:
            f.write(f"content num check{i}")

existing_buckets = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
if bucket_name not in existing_buckets:
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
    )

print("Starting upload of daily documents…")

for file_name in os.listdir(folder_path):
    file_path = join(folder_path, file_name)
    if isfile(file_path):
        s3.upload_file(file_path, bucket_name, file_name)
        print(file_name)

