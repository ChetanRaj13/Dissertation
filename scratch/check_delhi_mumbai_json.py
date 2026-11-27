import json

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Delhi districts in nationwide json:")
for d in data:
    if d['state'].lower() == 'delhi':
        print(f"  {d['district']}: {d['stage_of_extraction_pct']}% (cat: {d['category']})")

print("\nMaharashtra Mumbai districts in nationwide json:")
for d in data:
    if d['state'].lower() == 'maharashtra' and 'mumbai' in d['district'].lower():
        print(f"  {d['district']}: {d['stage_of_extraction_pct']}% (cat: {d['category']})")
