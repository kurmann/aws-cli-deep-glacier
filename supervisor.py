import argparse
from scripts.list_buckets import list_buckets
from scripts.check_restore_status import check_restore_status

def main():
    parser = argparse.ArgumentParser(
        description="Supervisor für S3 Restore Utilities",
        epilog="Beispielaufrufe: \n"
               "  python3 supervisor.py list_buckets\n"
               "  python3 supervisor.py check_restore_status <bucket_name> <directory_path>"
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

    args = parser.parse_args()

    if hasattr(args, 'func'):
        if args.command == 'list_buckets':
            args.func()
        elif args.command == 'check_restore_status':
            args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
