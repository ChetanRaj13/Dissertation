import urllib.request
import urllib.parse
import json
import time

queries = [
    ('Prestige Tech Cloud, Navarathna Agrahara, Bengaluru', 'Prestige Tech Cloud, Navarathna Agrahara, Bengaluru'),
    ('Navarathna Agrahara, Bengaluru', 'Navarathna Agrahara, Bengaluru'),
    ('Khajisonnenahalli, Bengaluru', 'Khajisonnenahalli, Bengaluru'),
    ('Electronic City Phase 1, Bengaluru', 'Electronic City Phase 1, Bengaluru'),
    ('Veersandra, Electronic City, Bengaluru', 'Veersandra, Electronic City, Bengaluru'),
    ('EPIP Zone, Whitefield, Bengaluru', 'EPIP Zone, Whitefield, Bengaluru'),
    ('Hoskote Industrial Area, Karnataka', 'Hoskote Industrial Area, Karnataka'),
    ('Cyber Park, Electronic City, Bengaluru', 'Cyber Park, Electronic City, Bengaluru'),
    ('KIADB Aerospace Park, Devanahalli', 'KIADB Aerospace Park, Devanahalli'),
    ('Pattandur Agrahara, Whitefield, Bengaluru', 'Pattandur Agrahara, Whitefield, Bengaluru'),
    ('International Tech Park Bangalore, Whitefield', 'International Tech Park Bangalore, Whitefield'),
    ('Whitefield, Bengaluru', 'Whitefield, Bengaluru')
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
