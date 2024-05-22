# S3 Restore Utilities

Dieses Repository enthält Python-Skripte, die bei der Verwaltung von S3-Buckets und der Wiederherstellung von Objekten aus Glacier helfen.

## Verwendung des Docker-Images

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

Docker Compose ermöglicht es, Multi-Container-Docker-Anwendungen einfach zu definieren und auszuführen. Hier ist die aktualisierte `docker-compose.yml`, die das Docker-Image direkt aus Docker Hub verwendet.

### Docker Compose einrichten

1. **Erstelle eine `docker-compose.yml` im Root-Verzeichnis**:
   ```yaml
   services:
     s3-restore-utilities:
       image: kurmann/s3-restore-utilities:latest
       container_name: s3-restore-utilities
       volumes:
         - /volume1/docker/s3-restore-utilities/downloads:/usr/src/app/downloads
         - /volume1/docker/s3-restore-utilities/logs:/usr/src/app/logs
       env_file:
         - .env
       entrypoint: ["python3", "/usr/src/app/supervisor.py"]
       tty: true
       stdin_open: true

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
   docker-compose up
   ```

5. **Docker Compose im Hintergrund ausführen**:
   ```bash
   docker-compose up -d
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
- **Leistung**: Volumes bieten eine bessere Leistung im Vergleich zu Bind-Mounts, insbesondere bei vielen I/O-Operationen.

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

Die Skripte werden über das `supervisor.py`-Skript aufgerufen, das sich im Root des Docker-Arbeitsverzeichnisses befindet. Verwende den `--help`-Parameter, um Informationen zu den erforderlichen Parametern für jedes Skript zu erhalten.

#### Restore Deep Glacier

Dieses Skript initiiert die Wiederherstellung aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen aus Glacier.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, das du wiederherstellen möchtest.
- `glacier-tier`: Die gewünschte Wiederherstellungs-Tier (`Bulk`, `Standard`, `Expedited`).

**Beispielaufruf:**

```bash
docker-compose run s3-restore-utilities restore_deep_glacier dein-bucket-name pfad/zum/verzeichnis --glacier_tier Bulk
```

#### List Buckets

Dieses Skript listet alle S3-Buckets in deinem AWS-Konto auf.

**Beispielaufruf:**

```bash
docker-compose run s3-restore-utilities list_buckets
```

#### Check Restore Status

Dieses Skript überprüft den Wiederherstellungsstatus aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen. Es gibt die Anzahl der Dateien aus, die wiederhergestellt werden können und jene, die es nicht können, und listet die Dateien gruppiert auf. Ein Fortschrittsbalken zeigt den Überprüfungsfortschritt an.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, dessen Wiederherstellungsstatus du überprüfen möchtest.

**Beispielaufruf:**

```bash
docker-compose run s3-restore-utilities check_restore_status dein-bucket-name pfad/zum/verzeichnis
```

#### Download S3 Directory

Dieses Skript lädt ein gesamtes Verzeichnis aus einem S3-Bucket herunter.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `s3-directory`: Der Pfad zum Verzeichnis, das du herunterladen möchtest.
- `local-directory`: Der lokale Pfad, in den die Dateien heruntergeladen werden sollen.

**Beispielaufruf:**

```bash
docker-compose run s3-restore-utilities download_s3_directory dein-bucket-name pfad/zum/verzeichnis lokaler-pfad
```

### Docker Logs

Du kannst die Logs der Skripte in Echtzeit überwachen, indem du die Docker-Logs verwendest. Dies ist besonders nützlich, um den Fortschritt und mögliche Fehler zu sehen.

**Logs in Echtzeit überwachen:**

```bash
docker-compose logs -f
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der `LICENSE`-Datei.