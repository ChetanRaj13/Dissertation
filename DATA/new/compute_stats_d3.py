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

hyd_records = [r for r in records if r.get("city_or_town") == "Hyderabad" or r.get("district") == "Ranga Reddy"]
hyd_op = sum(r.get("operational_mw") or 0.0 for r in hyd_records)
print(f"\nHyderabad records count: {len(hyd_records)}")
print(f"Hyderabad operational MW: {hyd_op:.1f}")
for r in hyd_records:
    print(f"  {r['id']}: {r['facility_name']} | op={r.get('operational_mw')} | pl={r.get('planned_ultimate_mw')} | status={r.get('true_development_status')}")
