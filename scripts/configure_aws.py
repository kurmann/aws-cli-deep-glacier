import os
import subprocess

def configure_aws():
    """Konfiguriert die AWS CLI mit Zugangsdaten."""
    print("AWS CLI ist nicht konfiguriert. Bitte gib deine AWS-Zugangsdaten ein.")
    aws_access_key_id = input("AWS Access Key ID: ").strip()
    aws_secret_access_key = input("AWS Secret Access Key: ").strip()
    aws_default_region = input("AWS Region (Standard: eu-west-1): ").strip()
    if not aws_default_region:
        aws_default_region = "eu-west-1"
    
    commands = [
        f"aws configure set aws_access_key_id {aws_access_key_id}",
        f"aws configure set aws_secret_access_key {aws_secret_access_key}",
        f"aws configure set region {aws_default_region}"
    ]

    for command in commands:
        os.system(command)
    
    print("AWS CLI Konfiguration abgeschlossen.")
    print("Starte das Hauptskript erneut...")
    script_dir = os.path.dirname(os.path.realpath(__file__))
    start_script = os.path.join(script_dir, 'start.py')
    subprocess.run(['python3', start_script])

if __name__ == "__main__":
    configure_aws()