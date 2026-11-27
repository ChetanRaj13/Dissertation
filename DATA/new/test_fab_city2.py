import urllib.request
import urllib.parse
import json
import time

queries = [
    ('Raviryal Ranga Reddy', 'Raviryal'),
    ('Raviryala Ranga Reddy', 'Raviryala'),
    ('Fab City Hyderabad', 'Fab City'),
    ('TSIIC Raviryal', 'Raviryal village'),
    ('Maheshwaram Ranga Reddy', 'Maheshwaram, Ranga Reddy')
]

headers = {'User-Agent': 'TISS-Dissertation-Data-Verification/1.0 (academic-research)'}

for name, q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json&limit=5"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            for item in data:
                if 'Telangana' in item['display_name']:
                    print(f"MATCH: {name} -> {item['lat']}, {item['lon']} | {item['display_name']}")
    except Exception as e:
        print(f"{name} -> ERROR: {e}")
    time.sleep(1.2)
