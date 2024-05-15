import boto3
import sys

def check_restore_status(bucket_name, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            try:
                head_object = s3.head_object(Bucket=bucket_name, Key=key)
                restore_status = head_object.get('Restore')
                if restore_status:
                    print(f"{key}: {restore_status}")
                else:
                    print(f"{key}: No restore in progress")
            except Exception as e:
                print(f"Fehler beim Überprüfen des Wiederherstellungsstatus von {key}: {e}")
    else:
        print("Keine Objekte gefunden.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <bucket-name> <prefix>")
    else:
        bucket_name = sys.argv[1]
        prefix = sys.argv[2]
        check_restore_status(bucket_name, prefix)
