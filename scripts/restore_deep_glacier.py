import boto3
import sys

# AWS S3-Konfigurationsvariablen
BUCKET_NAME = 'dein-bucket-name'
PREFIX = 'pfad/zum/verzeichnis/'  # Der Pfad zum Verzeichnis, das du wiederherstellen möchtest
RESTORE_DAYS = 7
GLACIER_TIER = 'Bulk'  # Mögliche Werte: 'Bulk', 'Standard', 'Expedited'

def restore_objects(bucket_name, prefix, restore_days, glacier_tier):
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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <bucket-name> <prefix> <glacier-tier>")
    else:
        BUCKET_NAME = sys.argv[1]
        PREFIX = sys.argv[2]
        GLACIER_TIER = sys.argv[3]
        restore_objects(BUCKET_NAME, PREFIX, RESTORE_DAYS, GLACIER_TIER)
