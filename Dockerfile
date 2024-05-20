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

# Erstelle die Profildateien mit den Startbefehlen
RUN echo 'echo "Willkommen zu den S3 Restore Utilities!"' >> ~/.profile && \
    echo 'python3 /usr/src/app/scripts/start.py' >> ~/.profile && \
    echo 'echo "Willkommen zu den S3 Restore Utilities!"' >> ~/.bashrc && \
    echo 'python3 /usr/src/app/scripts/start.py' >> ~/.bashrc && \
    echo 'echo "Willkommen zu den S3 Restore Utilities!"' >> ~/.zshrc && \
    echo 'python3 /usr/src/app/scripts/start.py' >> ~/.zshrc && \
    echo 'echo "Willkommen zu den S3 Restore Utilities!"' >> ~/.shrc && \
    echo 'python3 /usr/src/app/scripts/start.py' >> ~/.shrc

# Verlinke die .shrc in .profile, um sicherzustellen, dass die Einstellungen geladen werden
RUN echo 'if [ -f ~/.shrc ]; then . ~/.shrc; fi' >> ~/.profile

# Starte das Startskript und öffne danach eine Shell
ENTRYPOINT ["sh", "-c", "echo 'Willkommen zu den S3 Restore Utilities!' && python3 /usr/src/app/scripts/start.py && exec sh"]
