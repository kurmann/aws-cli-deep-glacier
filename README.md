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

## Verfügbare Skripte

### Restore Deep Glacier

**Script-Datei:** `restore_deep_glacier.py`

Dieses Skript initiiert die Wiederherstellung aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen aus Glacier.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, das du wiederherstellen möchtest.
- `glacier-tier`: Die gewünschte Wiederherstellungs-Tier (`Bulk`, `Standard`, `Expedited`).

**Beispielaufruf:**

```bash
python3 restore_deep_glacier.py dein-bucket-name pfad/zum/verzeichnis Bulk
```

### List Buckets

**Script-Datei:** `list_buckets.py`

Dieses Skript listet alle S3-Buckets in deinem AWS-Konto auf.

**Beispielaufruf:**

```bash
python3 list_buckets.py
```

### Check Restore Status

**Script-Datei:** `check_restore_status.py`

Dieses Skript überprüft den Wiederherstellungsstatus aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen. Es gibt die Anzahl der Dateien aus, die wiederhergestellt werden können und jene, die es nicht können, und listet die Dateien gruppiert auf. Ein Fortschrittsbalken zeigt den Überprüfungsfortschritt an.

**Eingabeparameter:**

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, dessen Wiederherstellungsstatus du überprüfen möchtest.

**Beispielaufruf:**

```bash
python3 check_restore_status.py dein-bucket-name pfad/zum/verzeichnis
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der `LICENSE`-Datei.
