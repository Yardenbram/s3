import boto3

bucket_name = 'student-yarden-bucket12'
region = 'us-west-2'
file_path = '/home/Yarden/.venv/team_image.png'
s3_key = 'team_image.png'

s3 = boto3.client('s3', region_name=region)

s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={'LocationConstraint': region}
)

print(f"Bucket '{bucket_name}' has been created.")

s3.upload_file(file_path, bucket_name, s3_key)

print("✅ File uploaded successfully!")

response = s3.list_objects_v2(Bucket=bucket_name)

print("📂 Files in bucket:")
if 'Contents' in response:
    for obj in response['Contents']:
        print("-", obj['Key'])
else:
    print("No files found.")
