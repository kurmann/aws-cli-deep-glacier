import boto3
import sys
from tqdm import tqdm

def check_restore_status(bucket_name, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    total_files = 0
    restorable_files = 0
    non_restorable_files = 0
    restorable = []
    non_restorable = []

    # Zähle alle Dateien und prüfe ihren Wiederherstellungsstatus
    for page in page_iterator:
        if 'Contents' in page:
            total_files += len(page['Contents'])

    print(f"Insgesamt zu prüfende Dateien: {total_files}")

    # Fortschrittsbalken initialisieren
    with tqdm(total=total_files, desc="Überprüfe Dateien", unit="Dateien") as pbar:
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    try:
                        head_object = s3.head_object(Bucket=bucket_name, Key=key)
                        restore_status = head_object.get('Restore')
                        if restore_status and 'ongoing-request="false"' in restore_status:
                            restorable_files += 1
                            restorable.append(key)
                        else:
                            non_restorable_files += 1
                            non_restorable.append(key)
                    except Exception as e:
                        print(f"Fehler beim Überprüfen des Wiederherstellungsstatus von {key}: {e}")
                    finally:
                        pbar.update(1)

    # Ergebnisse ausgeben
    print("\nZusammenfassung:")
    print(f"Dateien, die wiederhergestellt werden können: {restorable_files}")
    print(f"Dateien, die nicht wiederhergestellt werden können: {non_restorable_files}")

    print("\nWiederherstellbare Dateien:")
    for key in restorable:
        print(f"- {key}")

    print("\nNicht wiederherstellbare Dateien:")
    for key in non_restorable:
        print(f"- {key}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <bucket-name> <prefix>")
    else:
        bucket_name = sys.argv[1]
        prefix = sys.argv[2]
        check_restore_status(bucket_name, prefix)
