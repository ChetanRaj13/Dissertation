import json
import os
import re

base_dir = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\new"
json_path = os.path.join(base_dir, "verified_core_v2.json")
registry_path = os.path.join(base_dir, "url_registry_v2.txt")

# 1. Update url_registry_v2.txt
with open(registry_path, "r", encoding="utf-8") as f:
    reg_lines = f.readlines()

reg_urls = {line.split(" | ")[0].strip() for line in reg_lines if " | " in line}

missing_urls = [
    "https://datacenters.com | Global directory of colocation data centers | 2026-10-25\n",
    "https://datacentermap.com | Global colocation and data center mapping directory | 2026-10-25\n"
]

with open(registry_path, "a", encoding="utf-8") as f:
    for m in missing_urls:
        url_core = m.split(" | ")[0].strip()
        if url_core not in reg_urls:
            f.write(m)
            reg_urls.add(url_core)

# 2. Update gaps_or_conflicts in verified_core_v2.json with proximity explanations
with open(json_path, "r", encoding="utf-8") as f:
    records = json.load(f)

# Clusters sharing locality/village centroid:
# Rambilli: CORE01c, CORE08
# Chandanvelly: CORE13, CORE14
# Mahape: CORE19, CORE22
# Siruseri: CORE27, CORE31, CORE32, CORE35, CORE36
# Ambattur: CORE28, CORE30, CORE33, CORE38, CORE39

def add_proximity_note(rec, cluster_name, co_facilities):
    note = f"Proximity flag: Situated within {cluster_name} industrial cluster alongside {co_facilities}; shares the locality/village centroid."
    curr = rec.get("gaps_or_conflicts")
    if not curr:
        rec["gaps_or_conflicts"] = note
    elif "Proximity flag:" not in curr:
        rec["gaps_or_conflicts"] = curr + " " + note

for r in records:
    rid = r["id"]
    if rid in ["CORE01c", "CORE08"]:
        add_proximity_note(r, "Rambilli industrial corridor", "CORE01c/CORE08")
    elif rid in ["CORE13", "CORE14"]:
        add_proximity_note(r, "Chandanvelly industrial area", "CORE13/CORE14")
    elif rid in ["CORE19", "CORE22"]:
        add_proximity_note(r, "TTC Industrial Area (Mahape)", "CORE19/CORE22")
    elif rid in ["CORE27", "CORE31", "CORE32", "CORE35", "CORE36"]:
        add_proximity_note(r, "SIPCOT IT Park Siruseri", "CORE27, CORE31, CORE32, CORE35, CORE36")
    elif rid in ["CORE28", "CORE30", "CORE33", "CORE38", "CORE39"]:
        add_proximity_note(r, "Ambattur Industrial Estate", "CORE28, CORE30, CORE33, CORE38, CORE39")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print("Updated URL registry and added proximity explanations.")
