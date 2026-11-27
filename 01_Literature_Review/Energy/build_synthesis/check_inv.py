import json

with open('build_synthesis/inventory.json', 'r', encoding='utf-8') as f:
    inv = json.load(f)

print(f"Total inventory entries: {len(inv)}")
for item in inv:
    print(f"{item['id']}: {item['filename']} | pages: {item['page_count']} | size: {item['file_size']} bytes")
