import boto3
from scripts.configure_aws import configure_aws

def list_buckets():
    configure_aws()
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    print("Liste der S3-Buckets:")
    for bucket in response['Buckets']:
        print(f"- {bucket['Name']}")
