import json

for fname in ['DASHBOARD/groundwater_districts.json', 'DASHBOARD/nationwide_groundwater_extracted.json']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"File: {fname}")
        print(f"  Type: {type(data)}")
        if isinstance(data, list):
            print(f"  Count: {len(data)}")
            if len(data) > 0:
                print(f"  First item: {data[0]}")
        elif isinstance(data, dict):
            print(f"  Keys: {list(data.keys())[:10]}")
            first_k = list(data.keys())[0]
            print(f"  Sample [{first_k}]: {data[first_k]}")
    except Exception as e:
        print(f"Error reading {fname}: {e}")
