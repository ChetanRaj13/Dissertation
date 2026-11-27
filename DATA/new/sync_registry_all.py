import json

# 1. Load verified_core_v2.json
with open("verified_core_v2.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# 2. Collect every URL mentioned anywhere in any field of every record
all_urls = set()

for r in records:
    for k in ["district_source_url", "coordinate_source_url", "source_url", "google_maps_url"]:
        v = r.get(k)
        if v and isinstance(v, str) and v.startswith("http"):
            all_urls.add(v.strip())
            
    # Also parse sources field if it exists
    sources = r.get("sources") or []
    for s in sources:
        if isinstance(s, dict) and s.get("url"):
            all_urls.add(s["url"].strip())
        elif isinstance(s, str) and "http" in s:
            # extract url
            parts = s.split("http")
            for p in parts[1:]:
                clean_url = "http" + p.split(" ")[0].split(")")[0].split("]")[0].strip()
                all_urls.add(clean_url)

print(f"Total distinct URLs required across all fields: {len(all_urls)}")

# 3. Load existing registry
with open("url_registry_v2.txt", "r", encoding="utf-8") as f:
    existing = set(line.strip() for line in f if line.strip())

# 4. Find missing URLs
missing = all_urls - existing
print(f"Missing URLs from registry: {len(missing)}")

# 5. Append missing URLs to url_registry_v2.txt
if missing:
    with open("url_registry_v2.txt", "a", encoding="utf-8") as f:
        for u in sorted(missing):
            f.write(u + "\n")
    print(f"Appended {len(missing)} URLs to url_registry_v2.txt.")

# 6. Re-check
with open("url_registry_v2.txt", "r", encoding="utf-8") as f:
    final_urls = set(line.strip() for line in f if line.strip())

print(f"Total unique URLs now in registry: {len(final_urls)}")
