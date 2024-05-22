import argparse
from scripts.list_buckets import list_buckets
from scripts.check_restore_status import check_restore_status
from scripts.restore_deep_glacier import restore_objects
from scripts.download_s3_directory import download_s3_directory

def main():
    parser = argparse.ArgumentParser(
        description="Supervisor für S3 Restore Utilities",
        epilog="Beispielaufrufe: \n"
               "  python3 supervisor.py list_buckets\n"
               "  python3 supervisor.py check_restore_status <bucket_name> <directory_path>\n"
               "  python3 supervisor.py restore_deep_glacier <bucket_name> <prefix> [--glacier_tier <glacier_tier>]\n"
               "  python3 supervisor.py download_s3_directory <bucket_name> <s3_directory> <local_directory>"
    )
    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')

    # List Buckets
    parser_list_buckets = subparsers.add_parser('list_buckets', help='Listet alle S3-Buckets auf')
    parser_list_buckets.set_defaults(func=list_buckets)

    # Check Restore Status
    parser_check_restore_status = subparsers.add_parser('check_restore_status', help='Überprüft den Wiederherstellungsstatus')
    parser_check_restore_status.add_argument('bucket_name', type=str, help='Name des S3-Buckets')
    parser_check_restore_status.add_argument('directory_path', type=str, help='Pfad zum Verzeichnis')
    parser_check_restore_status.set_defaults(func=lambda args: check_restore_status(args.bucket_name, args.directory_path))

    # Restore Deep Glacier
    parser_restore_deep_glacier = subparsers.add_parser('restore_deep_glacier', help='Stellt Objekte aus Deep Glacier wieder her')
    parser_restore_deep_glacier.add_argument('bucket_name', type=str, help='Name des S3-Buckets')
    parser_restore_deep_glacier.add_argument('prefix', type=str, help='Pfad zum Verzeichnis')
    parser_restore_deep_glacier.add_argument('--glacier_tier', type=str, default='Bulk', help='Glacier-Tier (Bulk, Standard, Expedited)')
    parser_restore_deep_glacier.set_defaults(func=lambda args: restore_objects(args.bucket_name, args.prefix, glacier_tier=args.glacier_tier))

    # Download S3 Directory
    parser_download_s3_directory = subparsers.add_parser('download_s3_directory', help='Lädt ein S3-Verzeichnis herunter')
    parser_download_s3_directory.add_argument('bucket_name', type=str, help='Name des S3-Buckets')
    parser_download_s3_directory.add_argument('s3_directory', type=str, help='Pfad zum S3-Verzeichnis')
    parser_download_s3_directory.add_argument('local_directory', type=str, help='Lokaler Pfad zum Verzeichnis')
    parser_download_s3_directory.set_defaults(func=lambda args: download_s3_directory(args.bucket_name, args.s3_directory, args.local_directory))

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
