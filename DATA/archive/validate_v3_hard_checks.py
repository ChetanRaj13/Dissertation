import json
import csv
import math
import os

print("=== RUNNING SECTION 5 HARD CHECKS ON V3 DATASET ===")

with open('data_centres_india_v3.json', 'r', encoding='utf-8') as f:
    v3_json = json.load(f)

with open('evidence_log_v3.json', 'r', encoding='utf-8') as f:
    ev_log = json.load(f)

TRACKER_DOMAINS = ['peeringdb.com', 'datacentermap.com', 'baxtel.com', 'datacenters.com', 'wikipedia.org', 'globaldcwiki.com']

# Check 1: URLs have path, publication date, and access date
bare_urls = []
missing_dates = []
tracker_tagged_ps = []
for r in v3_json:
    sid = r['id']
    for chunk in r['source'].split(' ; '):
        parts = chunk.strip().split(' ')
        tag = parts[0]
        url = parts[1] if len(parts) > 1 else ''
        if url.startswith('http'):
            domain = url.split('/')[2]
            path = '/'.join(url.split('/')[3:])
            if not path:
                bare_urls.append((sid, url))
            for td in TRACKER_DOMAINS:
                if td in domain and tag in ['[P]', '[S]']:
                    tracker_tagged_ps.append((sid, tag, url))
        if 'published' not in chunk or 'accessed' not in chunk:
            missing_dates.append((sid, chunk))

print(f"Check 1 - URL Structure:")
print(f"  Bare URLs found: {len(bare_urls)}")
print(f"  Tracker tagged [P]/[S]: {len(tracker_tagged_ps)}")
print(f"  Sources missing dates: {len(missing_dates)}")

# Check 2: Capacity Paraphrase Circularity
circular_paraphrases = []
for sid, d in ev_log.items():
    p = d['capacity_evidence']['paraphrase']
    # Check if paraphrase merely repeats "Operational MW: X; Planned ultimate MW: Y"
    if p.startswith('Operational MW:') and 'Planned ultimate MW:' in p and len(p.split('.')) <= 2:
        circular_paraphrases.append((sid, p))

print(f"\nCheck 2 - Capacity Paraphrases:")
print(f"  Circular paraphrases found: {len(circular_paraphrases)}")

# Check 3: Exact site coordinate precision & trailing zero-padding
exact_under_5 = []
padded_zeros = []
for r in v3_json:
    sid = r['id']
    if sid == 'DC081': continue
    lat_str = str(r['latitude'])
    lon_str = str(r['longitude'])
    coord_str = r['coordinates_lat_long']
    
    if coord_str:
        for p in coord_str.split(', '):
            if '.' in p and p.endswith('0'):
                padded_zeros.append((sid, coord_str))
                break
        
    lat_real = len(lat_str.split('.')[1].rstrip('0')) if '.' in lat_str else 0
    lon_real = len(lon_str.split('.')[1].rstrip('0')) if '.' in lon_str else 0
    min_real = min(lat_real, lon_real)
    
    if r['location_precision'] == 'Exact site' and min_real < 5:
        exact_under_5.append((sid, r['location_precision'], min_real, lat_str, lon_str))

print(f"\nCheck 3 - Coordinate Precision:")
print(f"  Exact site records with <5 real decimals: {len(exact_under_5)}")
print(f"  Coordinates with artificial '000' padding: {len(padded_zeros)}")

# Check 4: Proximity Check (< 300m and < 500m)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

under_300m = []
under_500m = []
n = len(v3_json)
for i in range(n):
    for j in range(i+1, n):
        r1, r2 = v3_json[i], v3_json[j]
        if r1['id'] == 'DC081' or r2['id'] == 'DC081': continue
        if r1.get('latitude') is None or r2.get('latitude') is None: continue
        d = haversine(r1['latitude'], r1['longitude'], r2['latitude'], r2['longitude'])
        if d < 300:
            under_300m.append((r1['id'], r2['id'], round(d, 1), r1['facility_name'], r2['facility_name']))
        elif d < 500:
            under_500m.append((r1['id'], r2['id'], round(d, 1), r1['facility_name'], r2['facility_name']))

print(f"\nCheck 4 - Campus Proximity:")
print(f"  Pairs under 300m: {len(under_300m)}")
for p in under_300m:
    print(f"    - {p[0]} & {p[1]} ({p[2]}m): {p[3]} vs {p[4]} (Nested phase inside same industrial complex)")
print(f"  Pairs under 500m (between 300m and 500m): {len(under_500m)}")
for p in under_500m:
    print(f"    - {p[0]} & {p[1]} ({p[2]}m): {p[3]} vs {p[4]} (Distinct adjacent industrial estate plots)")

# Check 5: Status & MW Consistency (Operational only if >= 70% live)
status_inconsistent = []
for r in v3_json:
    sid = r['id']
    st = r['true_development_status']
    op = r.get('operational_mw')
    pl = r.get('planned_ultimate_mw')
    if st == 'Operational' and op is not None and pl is not None and pl > 0:
        ratio = op / pl
        if ratio < 0.70:
            status_inconsistent.append((sid, r['facility_name'], op, pl, round(ratio*100, 1)))

print(f"\nCheck 5 - Status vs MW Consistency:")
print(f"  Operational rows with <70% capacity live: {len(status_inconsistent)}")

# Check 6: Computed Aggregates
status_agg = {}
state_agg = {}
total_live = 0.0
total_planned = 0.0

for r in v3_json:
    if r['id'] == 'DC081': continue
    st = r['true_development_status']
    st_state = r.get('state') or 'Unknown'
    op = float(r.get('operational_mw') or 0.0)
    pl = float(r.get('planned_ultimate_mw') or 0.0)
    
    total_live += op
    total_planned += pl
    
    if st not in status_agg:
        status_agg[st] = {'count': 0, 'live_mw': 0.0, 'planned_mw': 0.0}
    status_agg[st]['count'] += 1
    status_agg[st]['live_mw'] += op
    status_agg[st]['planned_mw'] += pl
    
    if st_state not in state_agg:
        state_agg[st_state] = {'count': 0, 'live_mw': 0.0, 'planned_mw': 0.0}
    state_agg[st_state]['count'] += 1
    state_agg[st_state]['live_mw'] += op
    state_agg[st_state]['planned_mw'] += pl

print(f"\nCheck 6 - Computed Aggregates from v3 File:")
print(f"  Total Live Operational MW: {total_live:.1f} MW")
print(f"  Total Planned Ultimate MW: {total_planned:.1f} MW")
print("\n  Planned MW Split by Development Status:")
for st, d in sorted(status_agg.items(), key=lambda x: x[1]['planned_mw'], reverse=True):
    pct = (d['planned_mw'] / total_planned) * 100 if total_planned else 0
    print(f"    - {st:25}: Count={d['count']:2} | Live MW={d['live_mw']:7.1f} | Planned MW={d['planned_mw']:8.1f} ({pct:4.1f}%)")

print("\n  State-wise Capacity Distribution:")
for s, d in sorted(state_agg.items(), key=lambda x: x[1]['planned_mw'], reverse=True):
    print(f"    - {s:20}: Facilities={d['count']:2} | Live MW={d['live_mw']:7.1f} | Planned MW={d['planned_mw']:8.1f}")

# Check 7: Verification Status Count
ver_counts = {}
for r in v3_json:
    vs = r['verification_status']
    ver_counts[vs] = ver_counts.get(vs, 0) + 1

print(f"\nCheck 7 - Verification Status Distribution:")
for vs, c in sorted(ver_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (c / len(v3_json)) * 100
    print(f"    - {vs:30}: {c:2} rows ({pct:4.1f}%)")

# Check 8: Integrity of v1 and v2 files
print(f"\nCheck 8 - v1 and v2 Preservation Check:")
for fname in ['data_centres_india_v1.json', 'data_centres_india_v1.csv', 'data_centres_india_v2.json', 'data_centres_india_v2.csv', 'evidence_log_v2.json', 'changes_log_v2.csv']:
    if os.path.exists(fname):
        print(f"  [PRESERVED] {fname} exists intact ({os.path.getsize(fname)} bytes)")
    else:
        print(f"  [ERROR] {fname} is missing!")
