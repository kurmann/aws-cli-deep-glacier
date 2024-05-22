import boto3
from scripts.configure_aws import configure_aws

# AWS S3-Konfigurationsvariablen
DEFAULT_GLACIER_TIER = 'Bulk'  # Mögliche Werte: 'Bulk', 'Standard', 'Expedited'
RESTORE_DAYS = 7

def restore_objects(bucket_name, prefix, restore_days=RESTORE_DAYS, glacier_tier=DEFAULT_GLACIER_TIER):
    s3 = boto3.client('s3')
    # Listet alle Objekte im angegebenen Verzeichnis und den Unterverzeichnissen auf
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            try:
                # Initiieren der Wiederherstellung für jedes Objekt
                s3.restore_object(
                    Bucket=bucket_name,
                    Key=key,
                    RestoreRequest={
                        'Days': restore_days,
                        'GlacierJobParameters': {
                            'Tier': glacier_tier
                        }
                    }
                )
                print(f"Wiederherstellung initiiert für {key}")
            except Exception as e:
                print(f"Fehler bei der Wiederherstellung von {key}: {e}")
    else:
        print("Keine Objekte gefunden.")
