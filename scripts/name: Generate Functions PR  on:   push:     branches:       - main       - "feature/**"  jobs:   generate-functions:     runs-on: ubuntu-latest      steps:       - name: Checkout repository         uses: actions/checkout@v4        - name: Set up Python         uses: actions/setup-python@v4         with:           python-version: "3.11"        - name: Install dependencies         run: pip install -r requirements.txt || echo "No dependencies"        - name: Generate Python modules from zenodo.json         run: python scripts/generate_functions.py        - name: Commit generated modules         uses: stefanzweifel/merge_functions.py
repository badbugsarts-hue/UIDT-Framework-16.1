# scripts/merge_functions.py
import json
import os
import subprocess

# Verzeichnis mit Branches angeben, falls lokal geklont
branches = subprocess.check_output(["git", "branch", "-r"]).decode().splitlines()
branches = [b.strip().replace("origin/", "") for b in branches if "HEAD" not in b]

merged_functions = {}

# Funktionen von allen Branches auslesen
for branch in branches:
    subprocess.run(["git", "checkout", branch])
    if not os.path.exists("zenodo.json"):
        continue
    with open("zenodo.json", "r") as f:
        data = json.load(f)
        for func in data.get("functions", []):
            name = func["name"]
            if name not in merged_functions:
                merged_functions[name] = func
            else:
                # Bei Konflikt: Code aus main priorisieren
                merged_functions[name]["code"] = merged_functions[name].get("code", func.get("code"))

# Haupt-JSON aktualisieren
with open("zenodo.json", "w") as f:
    json.dump({"functions": list(merged_functions.values())}, f, indent=2)

print(f"Merged {len(merged_functions)} unique functions from {len(branches)} branches.")

# Branch main zurückschalten
subprocess.run(["git", "checkout", "main"])
