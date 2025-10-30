import json5, os, shutil, glob, re, subprocess
from tabulate import tabulate
from github import Github

# --- Funktionen ---

def smart_partition_repair(content, filename_prefix="file"):
    repaired = content
    logs = []
    block_info = []
    block_counter = 0

    # Dummy-RegEx Partitionierung (kann an dein JSON angepasst werden)
    blocks = re.split(r'(\{.*?\}|\[.*?\])', content, flags=re.DOTALL)
    for block in blocks:
        if not block.strip():
            continue
        start = repaired.find(block)
        end = start + len(block)
        try:
            json5.loads(block)
            block_info.append({"block": block_counter, "start": start, "end": end,
                               "confidence": 1.0, "status": "OK", "subfile": ""})
        except Exception as e:
            subfile = f"{filename_prefix}_block{block_counter}.json"
            with open(subfile, "w", encoding="utf-8") as sf:
                sf.write(block)
            logs.append(f"Extracted faulty block to {subfile} at {start}-{end}: {str(e)}")
            replacement = '{}' if block.strip().startswith('{') else '[]'
            repaired = repaired[:start] + replacement + repaired[end:]
            block_info.append({"block": block_counter, "start": start, "end": end,
                               "confidence": 0.5, "status": "Extracted", "subfile": subfile})
        block_counter += 1

    # Gesamte Datei prüfen
    try:
        json5.loads(repaired)
    except:
        logs.append("Entire file invalid, replaced with empty dict")
        repaired = '{}'
        block_info.append({"block": -1, "start": 0, "end": len(content),
                           "confidence": 0.2, "status": "Replaced", "subfile": ""})
    return repaired, logs, block_info

# --- Git-Branch erstellen ---
branch_name = "fail-safe-json-repair-dashboard"
subprocess.run(["git", "checkout", "-b", branch_name], check=True)

# --- JSON-Dateien finden ---
json_files = glob.glob("**/*.json", recursive=True)
changed_files = []
dashboard_table = []

for fpath in json_files:
    backup_path = f"{fpath}.bak"
    if not os.path.exists(backup_path):
        shutil.copy(fpath, backup_path)

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    iteration = 0
    max_iterations = 5
    while iteration < max_iterations:
        repaired_content, repair_logs, block_info = smart_partition_repair(content, fpath.replace("/", "_"))
        min_score = min(b["confidence"] for b in block_info)
        if repaired_content == content or min_score >= 0.8:
            break
        content = repaired_content
        iteration += 1

    if content != open(fpath, "r", encoding="utf-8").read():
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        changed_files.append(fpath)

    for b in block_info:
        dashboard_table.append([fpath, b["block"], b["start"], b["end"],
                                b["confidence"], b["status"], b["subfile"]])

# --- Commit & Push ---
if changed_files:
    subprocess.run(["git", "add"] + changed_files, check=True)
    commit_result = subprocess.run(["git", "commit", "-m", "Fail-Safe JSON Repair + Dashboard"], check=False)

    if commit_result.returncode == 0:
        subprocess.run(["git", "push", "--set-upstream", "origin", branch_name], check=True)

        # PR erstellen (optional)
        g = Github(os.environ["GITHUB_TOKEN"])
        repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
        pr = repo.create_pull(
            title="Fail-Safe JSON Repair + Dashboard",
            body="Automated fail-safe repair of JSON files with block-level dashboard.",
            head=branch_name,
            base="main"
        )

        # PR Comment: Dashboard
        table_str = tabulate(dashboard_table,
                             headers=["File", "Block", "Start", "End", "Confidence", "Status", "Subfile"],
                             tablefmt="github")
        pr.create_issue_comment(f"### JSON Repair Dashboard\n\n{table_str}")

else:
    with open("logs.txt") as f:
    logs = f.readlines()
    for line in logs:
        # Hier kommt dein Code
        print(line)
