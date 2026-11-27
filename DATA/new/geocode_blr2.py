import urllib.request
import urllib.parse
import json
import time

queries = [
    ('Prestige Tech Cloud', 'Prestige Tech Cloud'),
    ('Doddajala, Bengaluru', 'Doddajala, Bengaluru'),
    ('Veerasandra, Bengaluru', 'Veerasandra, Bengaluru'),
    ('EPIP, Whitefield, Bengaluru', 'EPIP, Whitefield, Bengaluru'),
    ('EPIP, Bengaluru', 'EPIP, Bengaluru'),
    ('ITPL, Whitefield, Bengaluru', 'ITPL, Whitefield, Bengaluru'),
    ('International Technology Park, Bengaluru', 'International Technology Park, Bengaluru'),
    ('Aerospace Park, Bengaluru', 'Aerospace Park, Bengaluru'),
    ('Devanahalli, Bengaluru', 'Devanahalli, Bengaluru')
]

headers = {'User-Agent': 'TISS-Dissertation-Data-Verification/1.0 (academic-research)'}

for name, q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json&limit=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data:
                res = data[0]
                lat = res['lat']
                lon = res['lon']
                disp = res['display_name']
                print(f"{name} -> {lat}, {lon} | {disp} | {url}")
            else:
                print(f"{name} -> NOT FOUND | {url}")
    except Exception as e:
        print(f"{name} -> ERROR: {e}")
    time.sleep(1.2)
