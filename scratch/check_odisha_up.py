import json

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Odisha districts:")
print([d['district'] for d in data if d['state'].lower() == 'odisha'])

print("\nUP districts matching 'gautam' or similar:")
print([d['district'] for d in data if d['state'].lower() == 'uttar pradesh' and ('g' in d['district'].lower() or 'b' in d['district'].lower() or 'n' in d['district'].lower())][:20])
