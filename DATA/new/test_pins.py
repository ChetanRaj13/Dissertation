import urllib.request
import urllib.parse
import json
import time

queries = [
    'Plot 18, EPIP, Bengaluru',
    'Plot 111, EPIP, Bengaluru',
    'Export Promotion Industrial Park, Whitefield',
    'KIADB Export Promotion Industrial Park',
    'Web Werks Bangalore BLR1',
    'Tata Communications Whitefield',
    'Airtel Data Center Whitefield',
    'Discoverer Building, ITPB, Bengaluru',
    'International Tech Park, Whitefield Road',
    'Sadharmasathram Road, Pattandur Agrahara'
]

headers = {'User-Agent': 'TISS-Dissertation-Data-Verification/1.0 (academic-research)'}

for q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json&limit=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data:
                print(f"{q} -> {data[0]['lat']}, {data[0]['lon']} | {data[0]['display_name']} | {url}")
            else:
                print(f"{q} -> NOT FOUND | {url}")
    except Exception as e:
        print(f"{q} -> ERROR: {e}")
    time.sleep(1.2)
