import json

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for state in ['Odisha', 'Uttar Pradesh', 'West Bengal']:
    print(f"=== {state} districts in nationwide json ===")
    for d in data:
        if d['state'].lower() == state.lower():
            if any(k in d['district'].lower() for k in ['khor', 'khordha', 'gautam', 'buddha', 'noida', 'hooghly', 'hugli']):
                print(f"  {d['district']}: stage={d['stage_of_extraction_pct']}%, page={d['page']}")
            elif len(data) < 40:
                print(f"  {d['district']}")
