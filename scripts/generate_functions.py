# scripts/generate_functions.py
import json
import os

with open("zenodo.json") as f:
    data = json.load(f)

os.makedirs("uidt_functions", exist_ok=True)

for func in data.get("functions", []):
    name = func["name"].replace(" ", "_")
    code = func.get("code", "")
    with open(f"uidt_functions/{name}.py", "w") as f:
        f.write(code)

print(f"Generated {len(data.get('functions', []))} Python modules in uidt_functions/")
