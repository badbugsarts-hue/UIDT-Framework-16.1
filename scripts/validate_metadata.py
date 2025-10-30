import sys
import json

def validate_metadata(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("✅ Metadata valid!")
    except FileNotFoundError:
        print(f"⚠️ Datei nicht gefunden: {file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON-Fehler in {file_path}: {e}")
    except Exception as e:
        print(f"💥 Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_metadata(sys.argv[1])
    else:
        print("ℹ️ Nutzung: python scripts/validate_metadata.py metadata.json")
