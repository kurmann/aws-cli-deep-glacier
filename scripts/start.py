
import os

def main():
    print("Willkommen zu den S3 Restore Utilities!")
    print("Hier sind die verfügbaren Skripte:")
    print("1. Restore Deep Glacier")
    print("2. List Buckets")
    print("3. Check Restore Status")
    print("Wähle eine Option (1, 2 oder 3):")

    choice = input().strip()

    if choice == '1':
        bucket_name = input("Gib den Namen des S3-Buckets ein: ").strip()
        prefix = input("Gib den Pfad zum Verzeichnis ein, das du wiederherstellen möchtest: ").strip()
        glacier_tier = input("Gib die gewünschte Wiederherstellungs-Tier ein (Bulk, Standard, Expedited): ").strip()
        os.system(f"python3 scripts/restore_deep_glacier.py {bucket_name} {prefix} {glacier_tier}")
    elif choice == '2':
        os.system("python3 scripts/list_buckets.py")
    elif choice == '3':
        bucket_name = input("Gib den Namen des S3-Buckets ein: ").strip()
        prefix = input("Gib den Pfad zum Verzeichnis ein, dessen Wiederherstellungsstatus du überprüfen möchtest: ").strip()
        os.system(f"python3 scripts/check_restore_status.py {bucket_name} {prefix}")
    else:
        print("Ungültige Auswahl. Bitte starte das Skript erneut und wähle 1, 2 oder 3.")

if __name__ == "__main__":
    main()
