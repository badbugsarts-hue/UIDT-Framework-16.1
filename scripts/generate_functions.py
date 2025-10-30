# scripts/generate_functions.py
import json
import os

# JSON-Datei laden
with open("zenodo.json", "r") as f:
    data = json.load(f)

functions = data.get("functions", [])

# Zielverzeichnis für die generierten Module
package_dir = "uidt_functions"
os.makedirs(package_dir, exist_ok=True)

# __init__.py anlegen, um das Verzeichnis als Package nutzbar zu machen
init_file = os.path.join(package_dir, "__init__.py")
with open(init_file, "w") as f_init:
    f_init.write("# Auto-generated UIDT functions package\n")

# Jede Funktion als eigenes Modul generieren
for func in functions:
    name = func["name"]
    code = func.get("code", f"def {name}():\n    pass  # placeholder\n")
    filepath = os.path.join(package_dir, f"{name}.py")
    with open(filepath, "w") as f_out:
        f_out.write(code)

print(f"Generated {len(functions)} Python modules in {package_dir}/")
