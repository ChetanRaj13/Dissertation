import urllib.request
import urllib.parse
import json
import time

queries = [
    ('Pioneer Towers, Madhapur, Hyderabad', 'Pioneer Towers, Madhapur, Hyderabad'),
    ('Software Units Layout, Madhapur', 'Software Units Layout, Madhapur'),
    ('Financial District, Nanakramguda, Hyderabad', 'Financial District, Nanakramguda, Hyderabad'),
    ('Survey No 115, Nanakramguda, Hyderabad', 'Survey No 115, Nanakramguda, Hyderabad'),
    ('Nanakramguda, Hyderabad', 'Nanakramguda, Hyderabad'),
    ('Kokapet, Hyderabad', 'Kokapet, Hyderabad'),
    ('Kondapur, Hyderabad', 'Kondapur, Hyderabad'),
    ('ITPH, Madhapur, Hyderabad', 'ITPH, Madhapur, Hyderabad'),
    ('Fab City, Raviryal', 'Fab City, Raviryal'),
    ('Raviryal, Rangareddy', 'Raviryal, Rangareddy'),
    ('Maheshwaram, Rangareddy', 'Maheshwaram, Rangareddy')
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
