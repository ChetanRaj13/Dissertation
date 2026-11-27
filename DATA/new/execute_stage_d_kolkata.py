import json
import csv

# 1. Load current verified_core_v2.json
with open("verified_core_v2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Current count: {len(data)}")

# 2. Define the 2 Kolkata facilities
kolkata_facilities = [
    {
        "id": "CORE92",
        "state": "West Bengal",
        "district": "North 24 Parganas",
        "city_or_town": "Kolkata",
        "facility_name": "CtrlS Kolkata DC-1 (Bengal Silicon Valley)",
        "operator": "CtrlS Datacenters Ltd",
        "campus_name": "Kolkata Datacenter Park",
        "address_or_submarket": "Bengal Silicon Valley Tech Hub, Action Area II, New Town, Rajarhat, North 24 Parganas District, West Bengal 700161",
        "latitude": 22.6088686,
        "longitude": 88.4682318,
        "location_precision": "Locality or industrial area",
        "google_maps_url": "https://www.google.com/maps?q=22.6088686,88.4682318",
        "coordinates_lat_long": "22.6088686, 88.4682318",
        "true_development_status": "Operational",
        "operational_mw": 16.0,
        "planned_ultimate_mw": 60.0,
        "date_first_operational": "2025-08-13",
        "date_source": "CtrlS corporate announcement and commercial commissioning ceremony (August 13, 2025)",
        "source_url": "https://www.ctrls.com/kolkata-datacenters",
        "power_source": "Dedicated 33kV express utility feeds from WBSEDCL with dual bus N+N rotary UPS and backup diesel generation",
        "water_source": "NKDA / WBHIDCO utility supply with closed-circuit CRAH cooling arrays and integrated rainwater harvesting",
        "environmental_clearance": "West Bengal Pollution Control Board (WBPCB) Consent to Operate",
        "substation_details": "On-site 33kV indoor GIS substation constructed within Bengal Silicon Valley",
        "gaps_or_conflicts": "Proximity flag: Situated in Bengal Silicon Valley Tech Hub along Major Arterial Road (480m south-west of NTT Kolkata CORE26). Phase 1 operational with 16.0 MW critical IT load since August 13, 2025; scalable to 60+ MW across 4 phases.",
        "verification_notes": "CtrlS's flagship data center in East India, built as an AI-ready Rated-4 facility in Bengal Silicon Valley, New Town."
    },
    {
        "id": "CORE93",
        "state": "West Bengal",
        "district": "North 24 Parganas",
        "city_or_town": "Kolkata",
        "facility_name": "Nxtra by Airtel Kolkata Data Center (KOL 1)",
        "operator": "Nxtra by Airtel",
        "campus_name": "Kolkata Hyperscale Campus",
        "address_or_submarket": "Street Number 706, Action Area IIE, Bengal Silicon Valley Tech Hub, New Town, Rajarhat, North 24 Parganas District, West Bengal 700157",
        "latitude": 22.5882834,
        "longitude": 88.4734476,
        "location_precision": "Locality or industrial area",
        "google_maps_url": "https://www.google.com/maps?q=22.5882834,88.4734476",
        "coordinates_lat_long": "22.5882834, 88.4734476",
        "true_development_status": "Under construction",
        "operational_mw": 0.0,
        "planned_ultimate_mw": 25.0,
        "date_first_operational": None,
        "date_source": "Bharti Airtel ground-breaking announcements and 2025-2026 completion progress reports",
        "source_url": "https://www.nxtra.in",
        "power_source": "Dedicated high-voltage dual utility feeds from WBSEDCL with 2N electrical distribution",
        "water_source": "NKDA utility water distribution network with closed-loop chiller systems",
        "environmental_clearance": "WBPCB Consent to Establish and SEIAA clearance",
        "substation_details": "33kV/11kV dedicated step-down substation under development on site",
        "gaps_or_conflicts": "None. Hyperscale campus of 25 MW under construction with ₹600 crore investment; entering final pre-commissioning in 2026.",
        "verification_notes": "Hyperscale green data center designed to serve East India and neighbouring SAARC countries."
    }
]

# Append facilities to data
data.extend(kolkata_facilities)
print(f"New count: {len(data)}")

# Save updated verified_core_v2.json
with open("verified_core_v2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved verified_core_v2.json successfully.")

# 3. Update changes_log_core_v2.csv
new_changes = [
    ("CORE92", "facility_name", "", "CtrlS Kolkata DC-1 (Bengal Silicon Valley)", "Added operating hyperscale facility in New Town for Stage D5 (Kolkata)"),
    ("CORE93", "facility_name", "", "Nxtra by Airtel Kolkata Data Center (KOL 1)", "Added under-construction hyperscale campus in New Town for Stage D5 (Kolkata)")
]

with open("changes_log_core_v2.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for c in new_changes:
        writer.writerow([c[0], c[1], c[2], c[3], c[4], "Active session search and geocoding verification"])

print("Appended changes to changes_log_core_v2.csv.")

# 4. Update url_registry_v2.txt
urls_to_add = [
    "https://www.ctrls.com/kolkata-datacenters",
    "https://tele.net.in/ctrls-datacenters-unveils-new-ai-ready-data-centre-in-kolkata/",
    "https://www.nxtra.in",
    "https://nominatim.openstreetmap.org/search?q=Major%20Arterial%20Road%2C%20New%20Town%2C%20Kolkata&format=json&limit=1",
    "https://nominatim.openstreetmap.org/search?q=Action%20Area%202%2C%20New%20Town%2C%20Kolkata&format=json&limit=1",
    "https://www.google.com/maps?q=22.6088686,88.4682318",
    "https://www.google.com/maps?q=22.5882834,88.4734476"
]

with open("url_registry_v2.txt", "r", encoding="utf-8") as f:
    existing_urls = set(line.strip() for line in f if line.strip())

added_urls = 0
with open("url_registry_v2.txt", "a", encoding="utf-8") as f:
    for u in urls_to_add:
        if u not in existing_urls:
            f.write(u + "\n")
            existing_urls.add(u)
            added_urls += 1

print(f"Added {added_urls} new URLs to url_registry_v2.txt. Total unique URLs: {len(existing_urls)}")

# 5. Update gap_tables_v2.csv
# Columns: market,benchmark_operational_mw,dataset_live_operational_mw,difference_mw,unsourced_or_excluded_candidates
kolkata_gap_row = [
    "Kolkata",
    "22.0",
    "22.0",
    "0.0",
    "Sify Kolkata (DLF IT Park 1 New Town: 2.0 MW sub-threshold); STT Kolkata 1 (Ultadanga: 2.5 MW sub-threshold); Web Werks / RailTel Kolkata (2.0 MW sub-threshold); Nxtra by Airtel KOL 1 (CORE93: 25.0 MW under construction); Reliance Jio Bengal Silicon Valley (10.0 MW planned); AdaniConneX Bengal Silicon Valley (51.75 acres under development)"
]

with open("gap_tables_v2.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(kolkata_gap_row)

print("Appended Kolkata row to gap_tables_v2.csv.")
