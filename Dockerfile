# Verwende ein offizielles Python-Image als Basis
FROM python:3.13-rc-alpine3.19

# Setze das Arbeitsverzeichnis im Container
WORKDIR /usr/src/app

# Kopiere die requirements.txt und installiere die Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installiere die AWS CLI
RUN apk add --no-cache aws-cli

# Kopiere den restlichen Quellcode ins Arbeitsverzeichnis
COPY scripts/ ./scripts/

# Stelle sicher, dass die Skripte ausführbar sind
RUN chmod +x scripts/*.py

# Führe das Skript aus
CMD ["python3", "/usr/src/app/scripts/start.py"]