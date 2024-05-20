import subprocess
import os

def configure_aws():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    subprocess.run(['python3', os.path.join(script_dir, 'configure_aws.py')])

def main():
    configure_aws()  # AWS CLI konfigurieren

    print("Willkommen zu den S3 Restore Utilities!")
    print("Hier sind die verfügbaren Skripte:")
    print("1. Restore Deep Glacier")
    print("2. List Buckets")
    print("3. Check Restore Status")
    print("4. Download S3 Directory")
    print("Wähle eine Option (1, 2, 3 oder 4):")

    choice = input().strip()

    script_dir = os.path.dirname(os.path.realpath(__file__))

    if choice == '1':
        bucket_name = input("Gib den Namen des S3-Buckets ein: ").strip()
        prefix = input("Gib den Pfad zum Verzeichnis ein, das du wiederherstellen möchtest: ").strip()
        glacier_tier = input("Gib die gewünschte Wiederherstellungs-Tier ein (Bulk, Standard, Expedited): ").strip()
        subprocess.run(['python3', os.path.join(script_dir, 'restore_deep_glacier.py'), bucket_name, prefix, glacier_tier])
    elif choice == '2':
        subprocess.run(['python3', os.path.join(script_dir, 'list_buckets.py')])
    elif choice == '3':
        bucket_name = input("Gib den Namen des S3-Buckets ein: ").strip()
        prefix = input("Gib den Pfad zum Verzeichnis ein, dessen Wiederherstellungsstatus du überprüfen möchtest: ").strip()
        subprocess.run(['python3', os.path.join(script_dir, 'check_restore_status.py'), bucket_name, prefix])
    elif choice == '4':
        bucket_name = input("Gib den Namen des S3-Buckets ein: ").strip()
        s3_directory = input("Gib das S3-Verzeichnis ein, das heruntergeladen werden soll: ").strip()
        local_directory = input("Gib das lokale Verzeichnis ein, in das heruntergeladen werden soll: ").strip()
        subprocess.run(['python3', os.path.join(script_dir, 'download_s3_directory.py'), bucket_name, s3_directory, local_directory])
    else:
        print("Ungültige Auswahl. Bitte starte das Skript erneut und wähle 1, 2, 3 oder 4.")

if __name__ == "__main__":
    main()