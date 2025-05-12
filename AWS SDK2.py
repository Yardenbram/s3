

import boto3
from botocore.exceptions import ClientError


SRC_BUCKET = "project-src-yarden"          
DST_BUCKET = "project-dst-yardenbra"      
SNS_TOPIC_ARN = "arn:aws:sts::496747580578:assumed-role/voclabs/user3844032=Yardenjne@gmail.com"

s3 = boto3.resource("s3")
sns = boto3.client("sns")


def move_sr1_files() -> None:
    moved = []

    
    for obj in s3.Bucket(SRC_BUCKET).objects.filter(Prefix="/home/Yarden/.venv/customer-details/sr1-door"):
        dst_key = f"sr1-door/{obj.key.split('/')[-1]}"  
        try:
            
            s3.Object(DST_BUCKET, dst_key).copy(
                {"Bucket": SRC_BUCKET, "Key": obj.key}
            )
            
            s3.Object(SRC_BUCKET, obj.key).delete()
            print(f"Moved {obj.key} -> {dst_key}")
            moved.append(dst_key)
        except ClientError as err:
            print(f"ERROR while processing {obj.key}: {err}")

    
    if moved:
        message = f"{len(moved)} file(s) moved to '{DST_BUCKET}/sr1/': " + ", ".join(moved)
        sns.publish(TopicArn=SNS_TOPIC_ARN, Subject="S3 file-move complete", Message=message)
        print("Notification sent.")


if __name__ == "__main__":
    move_sr1_files()
