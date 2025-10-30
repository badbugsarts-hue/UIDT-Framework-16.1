import json
import sys
import os

metadata_dir = sys.argv[1]

for file_name in os.listdir(metadata_dir):
    if file_name.endswith(".json"):
        path = os.path.join(metadata_dir, file_name)
        try:
            with open(path, "r") as f:
                json.load(f)
            print(f"{file_name} is valid JSON")
        except json.JSONDecodeError as e:
            print(f"ERROR in {file_name}: {e}")
            sys.exit(1)
