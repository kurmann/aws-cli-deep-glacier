# Verwende ein offizielles Python-Image als Basis
FROM python:3.12-bullseye

# Setze das Arbeitsverzeichnis im Container
WORKDIR /usr/src/app

# Kopiere die requirements.txt und installiere die Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installiere die AWS CLI
RUN apt-get update && \
    apt-get install -y awscli && \
    apt-get clean

# Kopiere den restlichen Quellcode ins Arbeitsverzeichnis
COPY scripts/ ./scripts/

# Stelle sicher, dass die Skripte ausführbar sind
RUN chmod +x scripts/*.py

# Definiere den Befehl zum Starten des Containers im interaktiven Modus
CMD ["python3", "./scripts/start.py"]
