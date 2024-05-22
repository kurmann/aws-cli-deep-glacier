import os
import subprocess

def configure_aws():
    """Konfiguriert die AWS CLI mit Zugangsdaten aus Umgebungsvariablen."""
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_default_region = os.getenv('AWS_DEFAULT_REGION', 'eu-west-1')

    if not aws_access_key_id or not aws_secret_access_key:
        print("AWS_ACCESS_KEY_ID oder AWS_SECRET_ACCESS_KEY ist nicht gesetzt.")
        print("Bitte setze die Umgebungsvariablen AWS_ACCESS_KEY_ID und AWS_SECRET_ACCESS_KEY.")
        print("Bei Verwendung von Docker Composer kannst du die .env-Datei verwenden.")
        return

    commands = [
        f"aws configure set aws_access_key_id {aws_access_key_id}",
        f"aws configure set aws_secret_access_key {aws_secret_access_key}",
        f"aws configure set region {aws_default_region}"
    ]

    # Führe die AWS CLI-Konfigurationsbefehle aus und unterdrücke die Ausgabe auf der Konsole aus Sicherheitsgründen
    for command in commands:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("AWS CLI Konfiguration abgeschlossen.")
