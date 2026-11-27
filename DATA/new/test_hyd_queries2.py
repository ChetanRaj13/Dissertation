import urllib.request
import urllib.parse
import json
import time

queries = [
    ('The V Madhapur', 'The V, Madhapur, Hyderabad'),
    ('Ascendas Hyderabad', 'Ascendas, Madhapur'),
    ('CapitaLand Hyderabad', 'CapitaLand, Hyderabad'),
    ('Inorbit Mall Madhapur', 'Inorbit Mall, Madhapur'),
    ('Fab City Raviryal 1', 'Fab City, Srinagar'),
    ('Fab City 2', 'Fab City, Shamshabad'),
    ('Raviryal 3', 'Raviryala, Telangana'),
    ('Raviryal 4', 'Raviryal, Shamshabad'),
    ('Maheshwaram', 'Maheswaram, Ranga Reddy')
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
