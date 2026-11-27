import urllib.request
import urllib.parse
import json
import time

queries = [
    ('NTT Chandivali', 'Hiranandani Business Park, Chandivali, Mumbai'),
    ('CtrlS Mahape', 'TTC Industrial Area, Mahape, Navi Mumbai'),
    ('Sify Rabale', 'TTC Industrial Area, Rabale, Navi Mumbai'),
    ('Sify Airoli', 'Mindspace, Airoli, Navi Mumbai'),
    ('STT Navi Mumbai', 'Millennium Business Park, Mahape, Navi Mumbai'),
    ('STT BKC', 'Bandra Kurla Complex, Mumbai'),
    ('Nxtra Mahape', 'Electronic Zone, Mahape, Navi Mumbai'),
    ('Web Werks Rabale', 'Rabale MIDC, Navi Mumbai'),
    ('AdaniConneX Taloja', 'MIDC Industrial Area, Taloja'),
    ('CapitaLand Airoli', 'Digha, Airoli, Navi Mumbai'),
    ('Equinix Chandivali', 'Chandivali Farm Road, Andheri East, Mumbai'),
    ('Digital Edge Airoli', 'Airoli Knowledge Park, Navi Mumbai')
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
