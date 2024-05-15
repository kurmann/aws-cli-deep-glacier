# S3 Restore Utilities

Dieses Repository enthält drei Python-Skripte, die bei der Verwaltung von S3-Buckets und der Wiederherstellung von Objekten aus Glacier helfen.

## Voraussetzungen

- Python 3.x
- Boto3 (Python-Bibliothek)

## Installation

### Python-Abhängigkeiten installieren

1. Erstelle eine `requirements.txt`-Datei im Stammverzeichnis deines Projekts mit folgendem Inhalt:
   ```
   boto3
   ```

2. Installiere die Abhängigkeiten:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Scripts

### 1. `restore_deep_glacier.py`

Dieses Skript initiiert die Wiederherstellung aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen aus Glacier.

#### Eingabeparameter

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, das du wiederherstellen möchtest.
- `glacier-tier`: Die gewünschte Wiederherstellungs-Tier (`Bulk`, `Standard`, `Expedited`).

#### Beispielaufruf

```bash
python3 restore_deep_glacier.py dein-bucket-name pfad/zum/verzeichnis Bulk
```

### Code

```python
import boto3
import sys

# AWS S3-Konfigurationsvariablen
BUCKET_NAME = 'dein-bucket-name'
PREFIX = 'pfad/zum/verzeichnis/'  # Der Pfad zum Verzeichnis, das du wiederherstellen möchtest
RESTORE_DAYS = 7
GLACIER_TIER = 'Bulk'  # Mögliche Werte: 'Bulk', 'Standard', 'Expedited'

def restore_objects(bucket_name, prefix, restore_days, glacier_tier):
    s3 = boto3.client('s3')

    # Listet alle Objekte im angegebenen Verzeichnis und den Unterverzeichnissen auf
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            try:
                # Initiieren der Wiederherstellung für jedes Objekt
                s3.restore_object(
                    Bucket=bucket_name,
                    Key=key,
                    RestoreRequest={
                        'Days': restore_days,
                        'GlacierJobParameters': {
                            'Tier': glacier_tier
                        }
                    }
                )
                print(f"Wiederherstellung initiiert für {key}")
            except Exception as e:
                print(f"Fehler bei der Wiederherstellung von {key}: {e}")
    else:
        print("Keine Objekte gefunden.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <bucket-name> <prefix> <glacier-tier>")
    else:
        BUCKET_NAME = sys.argv[1]
        PREFIX = sys.argv[2]
        GLACIER_TIER = sys.argv[3]
        restore_objects(BUCKET_NAME, PREFIX, RESTORE_DAYS, GLACIER_TIER)
```

### 2. `list_buckets.py`

Dieses Skript listet alle S3-Buckets in deinem AWS-Konto auf.

#### Beispielaufruf

```bash
python3 list_buckets.py
```

### Code

```python
import boto3

def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    print("Liste der S3-Buckets:")
    for bucket in response['Buckets']:
        print(f"- {bucket['Name']}")

if __name__ == "__main__":
    list_buckets()
```

### 3. `check_restore_status.py`

Dieses Skript überprüft den Wiederherstellungsstatus aller Objekte in einem bestimmten Verzeichnis und dessen Unterverzeichnissen. Es gibt die Anzahl der Dateien aus, die wiederhergestellt werden können und jene, die es nicht können, und listet die Dateien gruppiert auf. Ein Fortschrittsbalken zeigt den Überprüfungsfortschritt an.

#### Eingabeparameter

- `bucket-name`: Der Name des S3-Buckets.
- `prefix`: Der Pfad zum Verzeichnis, dessen Wiederherstellungsstatus du überprüfen möchtest.

#### Abhängigkeiten

- Python 3.x
- `boto3`: AWS SDK for Python
- `tqdm`: Bibliothek zur Anzeige von Fortschrittsbalken

#### Installation der Abhängigkeiten

1. Erstelle eine `requirements.txt`-Datei im Stammverzeichnis deines Projekts mit folgendem Inhalt:
   ```
   boto3
   tqdm
   ```

2. Installiere die Abhängigkeiten:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

#### Beispielaufruf

```bash
python3 check_restore_status.py dein-bucket-name pfad/zum/verzeichnis
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der `LICENSE`-Datei.
