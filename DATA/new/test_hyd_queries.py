import urllib.request
import urllib.parse
import json
import time

queries = [
    ('Kokapet village', 'Kokapet, Gandipet mandal'),
    ('Kokapet SEZ', 'Kokapet, Ranga Reddy'),
    ('ITPH Madhapur', 'International Tech Park, Madhapur'),
    ('Cyber Gateway Madhapur (STT Hyd 1)', 'HITEC City, Madhapur'),
    ('STT Hyd 1 exact', 'Software Units Layout, HITEC City'),
    ('Nanakramguda Financial District', 'Financial District, Nanakramguda'),
    ('Sify Financial District', 'ISB Road, Nanakramguda'),
    ('Raviryala village', 'Raviryala, Maheswaram'),
    ('Fab City', 'Fabcity Road, Hyderabad'),
    ('Chandanvelly Adani', 'Chandanvalle, Telangana'),
    ('Chandanvelly general', 'Chandanvelly, Telangana')
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
