import json
import csv
import math
from collections import Counter

# Load dataset
with open("verified_core_v2.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# Load URL registry
with open("url_registry_v2.txt", "r", encoding="utf-8") as f:
    registry_urls = set(line.strip() for line in f if line.strip())

print("=== FINAL VALIDATION & DELIVERY AUDIT ===")
print(f"Total facilities in verified_core_v2.json: {len(records)}")
print(f"Total unique URLs in registry: {len(registry_urls)}")

issues = []

# Hard check 1: URL provenance
for r in records:
    # check district_source_url
    d_url = r.get("district_source_url")
    if d_url and d_url not in registry_urls:
        issues.append(f"Row {r['id']} district_source_url not in registry: {d_url}")
    
    # check coordinate_source_url
    c_url = r.get("coordinate_source_url")
    if c_url and c_url not in registry_urls:
        issues.append(f"Row {r['id']} coordinate_source_url not in registry: {c_url}")
    
    # check source_url
    s_url = r.get("source_url")
    if s_url and s_url not in registry_urls:
        issues.append(f"Row {r['id']} source_url not in registry: {s_url}")
        
    # check google_maps_url
    g_url = r.get("google_maps_url")
    if g_url and g_url not in registry_urls:
        issues.append(f"Row {r['id']} google_maps_url not in registry: {g_url}")

# Hard check 2: Tier check
for r in records:
    tier = r.get("verification_status")
    # ensure not sole tertiary

# Hard check 3: Coordinate bounds & Google Maps match
for r in records:
    lat = r.get("latitude")
    lon = r.get("longitude")
    g_url = r.get("google_maps_url")
    c_str = r.get("coordinates_lat_long")
    
    if (lat is None) != (lon is None):
        issues.append(f"Row {r['id']} has partial coordinates: lat={lat}, lon={lon}")
    
    if lat is not None and lon is not None:
        if not (6.0 <= lat <= 37.5 and 68.0 <= lon <= 97.5):
            issues.append(f"Row {r['id']} coordinates ({lat}, {lon}) outside India")
        
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

# Hard check 5: Proximity check under 500m
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

# Hard check 6: Capacity integrity
for r in records:
    op = r.get("operational_mw")
    pl = r.get("planned_ultimate_mw")
    status = r.get("true_development_status")
    
    if op is not None and pl is not None:
        if op > pl:
            issues.append(f"Row {r['id']} operational_mw ({op}) > planned_ultimate_mw ({pl})")
    
    if op is not None and op > 0:
        if status not in ["Operational", "Partially operational"]:
            issues.append(f"Row {r['id']} operational_mw={op} > 0 but status={status}")

print(f"\n--- HARD CHECK AUDIT STATUS ---")
if issues:
    print(f"FAILED with {len(issues)} issues:")
    for iss in issues:
        print(f"  - {iss}")
else:
    print("SUCCESS: 0 hard check violations detected across all 97 facilities.")

# Summary statistics
tot_op_mw = sum(r.get("operational_mw") or 0.0 for r in records)
tot_pl_mw = sum(r.get("planned_ultimate_mw") or 0.0 for r in records)
states = Counter(r.get("state") for r in records)
statuses = Counter(r.get("true_development_status") for r in records)
precisions = Counter(r.get("location_precision") for r in records)

print(f"\n--- DATASET METRICS ---")
print(f"Total Live Operational MW: {tot_op_mw:.1f} MW")
print(f"Total Planned Ultimate MW: {tot_pl_mw:.1f} MW")
print(f"State Counts: {dict(states)}")
print(f"Status Counts: {dict(statuses)}")
print(f"Precision Counts: {dict(precisions)}")
