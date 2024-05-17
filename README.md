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

## Verwendung

### Startskript

Ein neues Startskript (`start.py`) wurde hinzugefügt, das den Benutzer durch die verfügbaren Skripte führt. Es wird empfohlen, die AWS CLI-Konfiguration zuerst vorzunehmen, um sicherzustellen, dass alle Skripte ordnungsgemäß funktionieren.

**Start des Hauptskripts:**

```bash
python3 scripts/start.py
```

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
