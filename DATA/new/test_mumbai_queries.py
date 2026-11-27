import urllib.request
import urllib.parse
import json
import time

queries = [
    ('Chandivali', 'Chandivali, Mumbai'),
    ('Saki Vihar Road', 'Saki Vihar Road, Mumbai'),
    ('Mahape MIDC', 'Mahape, Navi Mumbai'),
    ('Rabale village', 'Rabale, Navi Mumbai'),
    ('Taloja MIDC', 'Taloja, Maharashtra'),
    ('Taloja Panvel', 'Taloja, Panvel'),
    ('Airoli MIDC', 'Airoli, Navi Mumbai')
]

headers = {'User-Agent': 'TISS-Dissertation-Data-Verification/1.0 (academic-research)'}

for name, q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json&limit=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                disp = data[0]['display_name']
                print(f"{name} ({q}) -> {lat}, {lon} | {disp} | {url}")
            else:
                print(f"{name} ({q}) -> NOT FOUND | {url}")
    except Exception as e:
        print(f"{name} ({q}) -> ERROR: {e}")
    time.sleep(1.2)
