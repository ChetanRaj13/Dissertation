import urllib.request
import urllib.parse
import json

queries = [
    ('Chandanvelly Industrial Park', 'Chandanvelly Industrial Park'),
    ('Chandanvelly SEZ', 'Chandanvelly, Ranga Reddy'),
    ('Shabad Ranga Reddy', 'Shabad, Ranga Reddy')
]

headers = {'User-Agent': 'TISS-Dissertation-Data-Verification/1.0 (academic-research)'}

for name, q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json&limit=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data:
                print(f"{name} -> {data[0]['lat']}, {data[0]['lon']} | {data[0]['display_name']}")
            else:
                print(f"{name} -> NOT FOUND")
    except Exception as e:
        print(f"{name} -> ERROR: {e}")
