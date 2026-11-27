import json
import csv
import os
import re
import math

base_dir = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\new"
json_path = os.path.join(base_dir, "verified_core_v2.json")
registry_path = os.path.join(base_dir, "url_registry_v2.txt")

with open(json_path, "r", encoding="utf-8") as f:
    records = json.load(f)

with open(registry_path, "r", encoding="utf-8") as f:
    reg_text = f.read()

reg_urls = set()
for line in reg_text.splitlines():
    if " | " in line:
        reg_urls.add(line.split(" | ")[0].strip())
    elif line.strip():
        reg_urls.add(line.strip())

print(f"Total records in v2: {len(records)}")
print(f"Total URLs in registry: {len(reg_urls)}")

issues = []

# Hard check 1: URL provenance
for r in records:
    d_url = r.get("district_source_url")
    if d_url and not any(d_url.startswith(u) or u.startswith(d_url) for u in reg_urls):
        issues.append(f"Row {r['id']} district_source_url {d_url} not in registry")
    
    c_url = r.get("coordinate_source_url")
    if c_url and not any(c_url.startswith(u) or u.startswith(c_url) for u in reg_urls):
        issues.append(f"Row {r['id']} coordinate_source_url {c_url} not in registry")
    
    for s in r.get("sources", []):
        match = re.search(r'https?://[^\s\)]+', s)
        if match:
            url = match.group(0)
            if not any(url.startswith(u) or u.startswith(url) for u in reg_urls):
                issues.append(f"Row {r['id']} source URL {url} not in registry")

# Hard check 2: No [T] source is only support
for r in records:
    sources = r.get("sources", [])
    tiers = [s[:3] for s in sources if len(s) >= 3]
    if tiers and all(t == "[T]" for t in tiers):
        issues.append(f"Row {r['id']} has only [T] sources")

# Hard check 3: Coordinates in India and state bounds, google_maps_url matches
for r in records:
    lat = r.get("latitude")
    lon = r.get("longitude")
    g_url = r.get("google_maps_url")
    c_str = r.get("coordinates_lat_long")
    
    if lat is not None and lon is not None:
        if not (6.0 <= lat <= 37.5 and 68.0 <= lon <= 97.5):
            issues.append(f"Row {r['id']} coordinates ({lat}, {lon}) outside India")
        
        # Match google maps URL
        expected_g = f"https://www.google.com/maps?q={lat},{lon}"
        if g_url != expected_g:
            issues.append(f"Row {r['id']} google_maps_url mismatch: {g_url} vs {expected_g}")
        
        expected_c = f"{lat}, {lon}"
        if c_str != expected_c:
            issues.append(f"Row {r['id']} coordinates_lat_long mismatch: {c_str} vs {expected_c}")

# Hard check 4: No trailing zero padding, Exact site >= 5 decimals
for r in records:
    lat = r.get("latitude")
    lon = r.get("longitude")
    prec = r.get("location_precision")
    
    if lat is not None and lon is not None:
        s_lat = str(lat)
        s_lon = str(lon)
        if ('.' in s_lat and s_lat.endswith('0')) or ('.' in s_lon and s_lon.endswith('0')):
            issues.append(f"Row {r['id']} has trailing zero: {s_lat}, {s_lon}")
        
        if prec == "Exact site":
            d_lat = len(s_lat.split('.')[1]) if '.' in s_lat else 0
            d_lon = len(s_lon.split('.')[1]) if '.' in s_lon else 0
            if d_lat < 5 or d_lon < 5:
                issues.append(f"Row {r['id']} Exact site has <5 decimals: {s_lat} ({d_lat}), {s_lon} ({d_lon})")

# Hard check 5: Proximity check under 500m (including <300m per Rule 60/108 explained with source/cluster)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

filled = [r for r in records if r.get("latitude") is not None and r.get("longitude") is not None]
for i in range(len(filled)):
    for j in range(i + 1, len(filled)):
        r1, r2 = filled[i], filled[j]
        if r1.get("parent_id") == r2["id"] or r2.get("parent_id") == r1["id"]:
            continue
        d = haversine(r1["latitude"], r1["longitude"], r2["latitude"], r2["longitude"])
        if d < 500:
            g1 = r1.get("gaps_or_conflicts") or ""
            g2 = r2.get("gaps_or_conflicts") or ""
            if "proximity" not in g1.lower() and "proximity" not in g2.lower():
                issues.append(f"Campuses under 500m unexplained: {r1['id']} ({r1['facility_name']}) and {r2['id']} ({r2['facility_name']}): {d:.1f}m")

# Hard check 6: operational_mw <= planned_ultimate_mw and MW > 0 implies Operational / Partially operational
for r in records:
    op = r.get("operational_mw")
    pl = r.get("planned_ultimate_mw")
    status = r.get("true_development_status")
    
    if op is not None and pl is not None:
        if op > pl:
            issues.append(f"Row {r['id']} operational_mw ({op}) > planned_ultimate_mw ({pl})")
    
    if op is not None and op > 0:
        if status not in ["Operational", "Partially operational"]:
            issues.append(f"Row {r['id']} has MW {op} > 0 but status is {status}")

print("\n--- HARD CHECK RESULTS ---")
if not issues:
    print("ALL HARD CHECKS PASSED WITH 0 VIOLATIONS!")
else:
    print(f"FAILED: Found {len(issues)} issues:")
    for iss in issues:
        print(f"  - {iss}")
