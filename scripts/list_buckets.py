import boto3

def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    print("Liste der S3-Buckets:")
    for bucket in response['Buckets']:
        print(f"- {bucket['Name']}")

if __name__ == "__main__":
    list_buckets()
