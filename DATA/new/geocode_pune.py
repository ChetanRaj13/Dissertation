import urllib.request
import urllib.parse
import json
import time

queries = [
    ('Dighi, Pune', 'Dighi, Pune'),
    ('Hinjewadi, Pune', 'Hinjewadi, Pune'),
    ('Kharadi, Pune', 'Kharadi, Pune'),
    ('Pimpri, Pune', 'Pimpri, Pune'),
    ('Morawadi, Pimpri, Pune', 'Morawadi, Pimpri, Pune'),
    ('Bhosari, Pune', 'Bhosari, Pune'),
    ('Darumbare, Pune', 'Darumbare, Pune'),
    ('Indialand Global Industrial Park, Hinjewadi', 'Indialand Global Industrial Park, Hinjewadi'),
    ('Phase 1, Hinjewadi, Pune', 'Phase 1, Hinjewadi, Pune'),
    ('Rajiv Gandhi Infotech Park, Hinjewadi', 'Rajiv Gandhi Infotech Park, Hinjewadi')
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
                print(f"{name} -> {lat}, {lon} | {disp} | {url}")
            else:
                print(f"{name} -> NOT FOUND | {url}")
    except Exception as e:
        print(f"{name} -> ERROR: {e}")
    time.sleep(1.2)
