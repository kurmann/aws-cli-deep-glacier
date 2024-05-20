
# S3 Restore Utilities

Dieses Repository enthält Python-Skripte, die bei der Verwaltung von S3-Buckets und der Wiederherstellung von Objekten aus Glacier helfen.

## Voraussetzungen

- Python 3.x
- Boto3 (AWS SDK for Python, für die Interaktion mit AWS-Diensten)
- TQDM (Bibliothek zur Anzeige von Fortschrittsbalken)

## Installation

### Python-Abhängigkeiten installieren

1. Erstelle eine `requirements.txt`-Datei im Stammverzeichnis deines Projekts mit folgendem Inhalt:
   ```
   boto3
   tqdm
   ```

2. Installiere die Abhängigkeiten:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

### Docker-Image verwenden

Du kannst ein Docker-Image verwenden, um die Skripte in einer isolierten Umgebung auszuführen. Das Docker-Image wird automatisch erstellt und auf Docker Hub veröffentlicht.

**Docker-Image ausführen:**

1. **Docker-Image ziehen:**
   ```bash
   docker pull kurmann/s3-restore-utilities:latest
   ```

2. **Docker-Container im interaktiven Modus starten:**
   ```bash
   docker run -it kurmann/s3-restore-utilities:latest
   ```

## Verwendung von Docker Compose

Docker Compose ermöglicht es, Multi-Container-Docker-Anwendungen einfach zu definieren und auszuführen. Hier sind die Schritte zur Nutzung von Docker Compose in verschiedenen Umgebungen, einschließlich Synology NAS.

### Docker Compose einrichten

1. **Erstelle eine `docker-compose.yml` im Root-Verzeichnis**:
   ```yaml
   version: '3.8'

   services:
     s3-restore-utilities:
       build:
         context: .
         dockerfile: Dockerfile
       container_name: s3-restore-utilities
       volumes:
         - /volume1/docker/s3-restore-utilities/downloads:/usr/src/app/downloads
         - /volume1/docker/s3-restore-utilities/logs:/usr/src/app/logs
       env_file:
         - .env
       tty: true

   volumes:
     downloads:
     logs:
   ```

2. **Erstelle eine `.env`-Datei im Root-Verzeichnis**:
   Kopiere die bereitgestellte `.env.example` und fülle deine AWS-Zugangsdaten aus:
   ```env
   AWS_ACCESS_KEY_ID=dein_access_key_id
   AWS_SECRET_ACCESS_KEY=dein_secret_access_key
   AWS_DEFAULT_REGION=eu-west-1
   ```

### Docker Compose auf einer Synology NAS verwenden

1. **Docker und Docker Compose installieren**:
   - Installiere Docker über das Paketzentrum auf deiner Synology NAS.
   - Docker Compose ist in der Regel bereits enthalten, falls nicht, kann es manuell installiert werden.

2. **Dateien auf die Synology NAS hochladen**:
   - Lade die `docker-compose.yml` und `.env`-Dateien über die File Station oder per SSH auf deine Synology NAS.

3. **Terminal (SSH) öffnen**:
   - Öffne ein Terminal zu deiner Synology NAS und navigiere zum Verzeichnis, in dem sich die `docker-compose.yml` befindet.

4. **Docker Compose ausführen**:
   ```bash
   docker-compose up --build
   ```

5. **Docker Compose im Hintergrund ausführen**:
   ```bash
   docker-compose up -d --build
   ```

### Überwachen der Container-Logs

Verwende den folgenden Befehl, um die Logs der Container in Echtzeit zu überwachen:
```bash
docker-compose logs -f
```

### Verwendung von `tty` in Docker Compose

- **`tty: true`**: Aktiviert einen pseudo-TTY im Container, wodurch der Container eine Terminal-Schnittstelle erhält.
- **Nutzen**: Dies ist besonders nützlich für interaktive Anwendungen oder Skripte, die Terminal-Eingaben erwarten.

### Volumes in Docker Compose

Volumes sind ein wichtiger Mechanismus in Docker, um Daten dauerhaft zu speichern und zwischen Containern zu teilen. 

#### Vorteile der Verwendung von Volumes:

- **Persistenz**: Daten in Volumes bleiben erhalten, auch wenn der Container gelöscht und neu erstellt wird.
- **Isolation**: Volumes isolieren Daten vom Container-Dateisystem, was die Verwaltung und Sicherung vereinfacht.
- **Leistung**: Volumes bieten eine bessere Leistung im Vergleich zur Bind-Mounts, insbesondere bei vielen I/O-Operationen.

#### Beispiel:

In der Docker Compose-Datei sind zwei Volumes definiert:

```yaml
volumes:
  downloads:
  logs:
```

Diese Volumes werden im Dienst `s3-restore-utilities` verwendet, um die Verzeichnisse `/usr/src/app/downloads` und `/usr/src/app/logs` im Container mit den entsprechenden Verzeichnissen auf dem Host zu verknüpfen:

```yaml
services:
  s3-restore-utilities:
    volumes:
      - /volume1/docker/s3-restore-utilities/downloads:/usr/src/app/downloads
      - /volume1/docker/s3-restore-utilities/logs:/usr/src/app/logs
```

Diese Konfiguration stellt sicher, dass Dateien, die in den Verzeichnissen `downloads` und `logs` gespeichert werden, auch nach dem Neustart oder der Neu-Erstellung des Containers erhalten bleiben.

### Verfügbare Skripte

#### Restore Deep Glacier

**Script-Datei:** `restore_deep_glacier.py`

Dieses Skript initiiert die Wiederherstellung aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen aus Glacier.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, das du wiederherstellen möchtest.
- `glacier-tier`: Die gewünschte Wiederherstellungs-Tier (`Bulk`, `Standard`, `Expedited`).

**Beispielaufruf:**

```bash
python3 scripts/restore_deep_glacier.py dein-bucket-name pfad/zum/verzeichnis Bulk
```

#### List Buckets

**Script-Datei:** `list_buckets.py`

Dieses Skript listet alle S3-Buckets in deinem AWS-Konto auf.

**Beispielaufruf:**

```bash
python3 scripts/list_buckets.py
```

#### Check Restore Status

**Script-Datei:** `check_restore_status.py`

Dieses Skript überprüft den Wiederherstellungsstatus aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen. Es gibt die Anzahl der Dateien aus, die wiederhergestellt werden können und jene, die es nicht können, und listet die Dateien gruppiert auf. Ein Fortschrittsbalken zeigt den Überprüfungsfortschritt an.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, dessen Wiederherstellungsstatus du überprüfen möchtest.

**Beispielaufruf:**

```bash
python3 scripts/check_restore_status.py dein-bucket-name pfad/zum/verzeichnis
```

#### AWS CLI Konfiguration

**Script-Datei:** `configure_aws.py`

Dieses Skript konfiguriert die AWS CLI mit den notwendigen Zugangsdaten. Es wird empfohlen, dieses Skript zuerst auszuführen, wenn die AWS CLI noch nicht konfiguriert ist.

**Beispielaufruf:**

```bash
python3 scripts/configure_aws.py
```

#### Download S3 Directory

**Script-Datei:** `download_s3_directory.py`

Dieses Skript lädt ein gesamtes Verzeichnis aus einem S3-Bucket herunter.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, das du herunterladen möchtest.
- `local-dir`: Der lokale Pfad, in den die Dateien heruntergeladen werden sollen.

**Beispielaufruf:**

```bash
python3 scripts/download_s3_directory.py dein-bucket-name pfad/zum/verzeichnis lokaler-pfad
```

### Docker Logs

Du kannst die Logs der Skripte in Echtzeit überwachen, indem du die Docker-Logs verwendest. Dies ist besonders nützlich, um den Fortschritt und mögliche Fehler zu sehen.

**Logs in Echtzeit überwachen:**

```bash
docker logs -f <container_id>
```

### Empfohlene Reihenfolge

1. Konfiguriere die AWS CLI:
   ```bash
   python3 scripts/configure_aws.py
   ```
2. Starte das Hauptskript:
   ```bash
   python3 scripts/start.py
   ```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der `LICENSE`-Datei.
