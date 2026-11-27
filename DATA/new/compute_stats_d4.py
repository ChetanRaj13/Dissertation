import json
from collections import Counter

with open("verified_core_v2.json", "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Total records: {len(records)}")

states = Counter(r.get("state") for r in records)
districts = Counter(r.get("district") for r in records)
statuses = Counter(r.get("true_development_status") for r in records)
precisions = Counter(r.get("location_precision") for r in records)
tot_op_mw = sum(r.get("operational_mw") or 0.0 for r in records)
tot_pl_mw = sum(r.get("planned_ultimate_mw") or 0.0 for r in records)

print(f"Total operational MW: {tot_op_mw:.1f}")
print(f"Total planned MW: {tot_pl_mw:.1f}")
print(f"States: {dict(states)}")
print(f"Statuses: {dict(statuses)}")
print(f"Precisions: {dict(precisions)}")

mumbai_records = [r for r in records if r.get("state") == "Maharashtra" and (r.get("district") in ["Thane", "Mumbai Suburban", "Mumbai City", "Raigad"] or "Mumbai" in r.get("city_or_town", ""))]
# Filter out Pune
mumbai_records = [r for r in mumbai_records if r.get("district") != "Pune"]
mumbai_op = sum(r.get("operational_mw") or 0.0 for r in mumbai_records)
print(f"\nMumbai records count: {len(mumbai_records)}")
print(f"Mumbai operational MW: {mumbai_op:.1f}")
for r in mumbai_records:
    print(f"  {r['id']}: {r['facility_name']} | op={r.get('operational_mw')} | pl={r.get('planned_ultimate_mw')} | status={r.get('true_development_status')}")
