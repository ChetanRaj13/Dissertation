import json

with open('DASHBOARD/nationwide_groundwater_extracted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total districts in nationwide file: {len(data)}")
states = set(d['state'] for d in data)
print(f"Unique states in nationwide file ({len(states)}):")
for s in sorted(states):
    count = sum(1 for d in data if d['state'] == s)
    print(f"  {s}: {count} districts")

# Let's check the 29 hosting districts in nationwide_groundwater_extracted.json
with open('DASHBOARD/groundwater_districts.json', 'r', encoding='utf-8') as f:
    gw_29 = json.load(f)

print(f"\nChecking 29 districts matching:")
for d in gw_29:
    # skip Bengaluru South
    if 'extra' in d.get('district', ''):
        continue
    # find match
    matches = [x for x in data if x['state'].lower() == d['state'].lower() and (x['district'].lower() == d['district'].lower() or d['cgwb_printed_name'].lower() in x['district'].lower() or x['district'].lower() in d['cgwb_printed_name'].lower())]
    if matches:
        m = matches[0]
        print(f"MATCH: {d['state']} - {d['district']} (stage: 29_file={d['stage_of_extraction_pct']}, nationwide={m['stage_of_extraction_pct']})")
    else:
        print(f"MISSING: {d['state']} - {d['district']} (printed: {d['cgwb_printed_name']})")
