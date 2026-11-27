import urllib.request
import urllib.parse
import json

queries = [
    'Road Number 7, EPIP, Bengaluru',
    'Road No 7, EPIP, Bengaluru',
    'EPIP Phase 1, Whitefield, Bengaluru',
    'EPIP Zone 1st Phase, Whitefield',
    'Export Promotion Industrial Park, Whitefield Road'
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
