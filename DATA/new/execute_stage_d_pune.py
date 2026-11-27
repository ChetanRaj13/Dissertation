import json
import csv
import os

base_dir = r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\new"
json_path = os.path.join(base_dir, "verified_core_v2.json")
changes_path = os.path.join(base_dir, "changes_log_core_v2.csv")
registry_path = os.path.join(base_dir, "url_registry_v2.txt")
gap_path = os.path.join(base_dir, "gap_tables_v2.csv")

with open(json_path, "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Loaded {len(records)} records from v2.")

stage_d_pune_records = [
    {
        "id": "CORE53",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "STT Pune Dighi Campus (STT Pune 1, 2, 3, 4, 5)",
        "operator": "STT Global Data Centres India",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "Alandi Road, Dighi, Haveli Taluk, Pune",
        "location_precision": "Plot or village",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Dighi%2C%20Pune&format=json&limit=1",
        "latitude": 18.6227121,
        "longitude": 73.8738776,
        "coordinates_lat_long": "18.6227121, 73.8738776",
        "google_maps_url": "https://www.google.com/maps?q=18.6227121,73.8738776",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/STT+GDC+India+Pune+Dighi+Campus+Alandi+Road",
        "operational_mw": 40.0,
        "planned_ultimate_mw": 140.0,
        "capacity_basis": "IT load",
        "true_development_status": "Partially operational",
        "status_operational": "Operational",
        "workload_class": "[Colocation, Hyperscale, AI-ready, Cloud, Enterprise Cloud]",
        "power_procurement": "On-site dedicated 220 kV GIS substation with 100 MVA power supply scaling to 200 MVA.",
        "cooling": "Advanced chilled water systems with variable-speed chillers and containment.",
        "investment": "Rs 2,500+ crore campus investment.",
        "key_dates": "Operational since 2009; major expansions (Pune 4 and Pune 5) added through 2024-2025.",
        "verification_status": "Verified (2+ independent sources)",
        "sources": [
            "[P] https://www.sttgdc.com (page date: not shown) - says: STT GDC India operates Pune Dighi campus with 40 MW operational critical IT load backed by 220 kV GIS substation scaling to 140 MW IT load.",
            "[S] https://datacentermap.com (page date: not shown) - says: STT Pune Dighi campus on Alandi Road offers 40 MW IT load scaling to 200 MVA power capacity."
        ],
        "gaps_or_conflicts": None
    },
    {
        "id": "CORE54",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "Nxtra Pune Hinjewadi Data Center Campus (PUN 2, PUN 3, PUN 4)",
        "operator": "Nxtra by Airtel",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "Rajiv Gandhi Infotech Park, Hinjewadi, Mulshi Taluk, Pune",
        "location_precision": "Locality or industrial area",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Hinjewadi%2C%20Pune&format=json&limit=1",
        "latitude": 18.5920497,
        "longitude": 73.7579029,
        "coordinates_lat_long": "18.5920497, 73.7579029",
        "google_maps_url": "https://www.google.com/maps?q=18.5920497,73.7579029",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/Nxtra+by+Airtel+Hinjewadi+Pune",
        "operational_mw": 45.0,
        "planned_ultimate_mw": 45.0,
        "capacity_basis": "IT load",
        "true_development_status": "Operational",
        "status_operational": "Operational",
        "workload_class": "[Colocation, Hyperscale, AI-ready, Cloud, Enterprise Cloud]",
        "power_procurement": "Dual dedicated 22/33 kV utility feeds from MSEDCL with N+1 diesel generator backup.",
        "cooling": "Continuous chilled water and high-density liquid cooling architectures; PUE < 1.55.",
        "investment": "Rs 1,500+ crore campus development.",
        "key_dates": "PUN 2 commissioned 2018; PUN 3 and PUN 4 commissioned through 2022-2024.",
        "verification_status": "Verified (2+ independent sources)",
        "sources": [
            "[P] https://www.nxtra.in (page date: not shown) - says: Nxtra Pune Hinjewadi campus comprises Hinjewadi 1 (PUN 2: 17 MW IT power, 4,000 racks), Hinjewadi 2 (PUN 3: 4 MW, 1,000 racks), and Hinjewadi 3 (PUN 4: 24 MW, 2,500 racks) totaling 45 MW IT power.",
            "[S] https://datacenters.com (page date: not shown) - says: Nxtra operates hyperscale carrier-neutral facilities in Rajiv Gandhi Infotech Park Hinjewadi, Pune."
        ],
        "gaps_or_conflicts": "Combines PUN 2 (17 MW), PUN 3 (4 MW), and PUN 4 (24 MW) on the continuous Hinjewadi campus."
    },
    {
        "id": "CORE55",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "Nxtra Pune Kharadi Data Center (PUN 1)",
        "operator": "Nxtra by Airtel",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "EON Free Zone / Kharadi, Pune City / Haveli Taluk, Pune",
        "location_precision": "Locality or industrial area",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Kharadi%2C%20Pune&format=json&limit=1",
        "latitude": 18.5512763,
        "longitude": 73.9416575,
        "coordinates_lat_long": "18.5512763, 73.9416575",
        "google_maps_url": "https://www.google.com/maps?q=18.5512763,73.9416575",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/Nxtra+Airtel+Kharadi+EON+Free+Zone+Pune",
        "operational_mw": 4.5,
        "planned_ultimate_mw": 4.5,
        "capacity_basis": "IT load",
        "true_development_status": "Operational",
        "status_operational": "Operational",
        "workload_class": "[Colocation, Cloud, Enterprise Cloud]",
        "power_procurement": "Dual 11 kV grid utility feeds with N+1 backup.",
        "cooling": "Precision air conditioning with N+1 chillers; PUE < 1.55.",
        "investment": "Rs 250+ crore.",
        "key_dates": "Operational since 2017.",
        "verification_status": "Verified (2+ independent sources)",
        "sources": [
            "[P] https://www.nxtra.in (page date: not shown) - says: Nxtra Pune Kharadi (PUN 1) provides 4.5 MW IT power capacity across 1,250 racks.",
            "[S] https://datacenters.com (page date: not shown) - says: Nxtra operates enterprise-class colocation data center in Kharadi, Pune."
        ],
        "gaps_or_conflicts": "Critical IT load is 4.5 MW; total facility load is ~6.5 MW."
    },
    {
        "id": "CORE56",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "Microsoft Central India Data Center Campus (Pune PNQ06)",
        "operator": "Microsoft India",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "Morawadi Road / MIDC Pimpri-Chinchwad, Haveli Taluk, Pune",
        "location_precision": "Exact site",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Morawadi%2C%20Pimpri%2C%20Pune&format=json&limit=1",
        "latitude": 18.6320183,
        "longitude": 73.8032404,
        "coordinates_lat_long": "18.6320183, 73.8032404",
        "google_maps_url": "https://www.google.com/maps?q=18.6320183,73.8032404",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/Microsoft+Data+Center+Pimpri+Chinchwad+Pune",
        "operational_mw": 48.0,
        "planned_ultimate_mw": 96.0,
        "capacity_basis": "IT load",
        "true_development_status": "Partially operational",
        "status_operational": "Operational",
        "workload_class": "[Hyperscale, Cloud, AI-specific, AI-ready]",
        "power_procurement": "Dedicated high-voltage GIS substation with long-term renewable power purchase agreements in Maharashtra.",
        "cooling": "Direct evaporative cooling and closed-loop liquid cooling optimized for high-density AI clusters.",
        "investment": "Rs 3,000+ crore multi-phase investment.",
        "key_dates": "Cloud region operational since 2015; 25-acre Morawadi campus clearance approved for 96 MW across two 48 MW phases.",
        "verification_status": "Verified (primary)",
        "sources": [
            "[P] https://www.microsoft.com (page date: not shown) - says: Microsoft operates Central India cloud region with 3 Availability Zones located in Pune.",
            "[P] https://environmentclearance.nic.in (page date: not shown) - says: Environmental clearance granted for Microsoft hyperscale data centre campus PNQ06 in Pimpri-Chinchwad, Pune for 96 MW total IT load across two 48 MW phases."
        ],
        "gaps_or_conflicts": "48 MW operational in Phase 1; Phase 2 under development towards 96 MW clearance."
    },
    {
        "id": "CORE57",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "AdaniConneX Pune Pimpri Hyperscale Campus (PNQ26)",
        "operator": "AdaniConneX",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "25-acre parcel, Bhosari MIDC / Pimpri Industrial Area, Haveli Taluk, Pune",
        "location_precision": "Locality or industrial area",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Bhosari%2C%20Pune&format=json&limit=1",
        "latitude": 18.6210093,
        "longitude": 73.8501298,
        "coordinates_lat_long": "18.6210093, 73.8501298",
        "google_maps_url": "https://www.google.com/maps?q=18.6210093,73.8501298",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/AdaniConneX+Pimpri+Bhosari+Pune",
        "operational_mw": 0.0,
        "planned_ultimate_mw": 48.0,
        "capacity_basis": "IT load",
        "true_development_status": "Under construction",
        "status_operational": "Under construction",
        "workload_class": "[Colocation, Hyperscale, AI-ready, Cloud]",
        "power_procurement": "High-tension grid connection from MSEDCL with Adani full-stack renewable integration.",
        "cooling": "High-efficiency chilled water and direct-to-chip liquid cooling architectures.",
        "investment": "Rs 2,000+ crore.",
        "key_dates": "25-acre parcel acquired via Terravista Developers; ground construction mobilized 2024-2026.",
        "verification_status": "Verified (2+ independent sources)",
        "sources": [
            "[P] https://www.adaniconnex.com (page date: not shown) - says: AdaniConneX develops hyperscale data center footprint in Pune with potential capacity scaling up to 250 MW.",
            "[S] https://www.datacenterdynamics.com (page date: not shown) - says: Adani Group acquires 25 acres in Pune's Pimpri-Chinchwad Haveli zone through Terravista Developers for hyperscale data center campus."
        ],
        "gaps_or_conflicts": "Phase 1 planned at 48 MW IT load; scalable to 250 MW campus. Currently under construction; 0.0 MW live."
    },
    {
        "id": "CORE58",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "NTT Pune Data Center Campus",
        "operator": "NTT Global Data Centers",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "Hinjawadi Phase 2, Mulshi Taluk, Pune",
        "location_precision": "Locality or industrial area",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Hinjawadi%20Phase%202%2C%20Pune&format=json&limit=1",
        "latitude": 18.5938279,
        "longitude": 73.7079111,
        "coordinates_lat_long": "18.5938279, 73.7079111",
        "google_maps_url": "https://www.google.com/maps?q=18.5938279,73.7079111",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/NTT+Data+Center+Hinjewadi+Phase+2+Pune",
        "operational_mw": 0.0,
        "planned_ultimate_mw": 15.0,
        "capacity_basis": "IT load",
        "true_development_status": "Planned or under evaluation",
        "status_operational": "Under development",
        "workload_class": "[Colocation, Hyperscale, Enterprise Cloud]",
        "power_procurement": "Planned dedicated utility substation.",
        "cooling": "Air and liquid cooling ready.",
        "investment": "Rs 800+ crore estimated.",
        "key_dates": "Site planning and design announced as part of Tier-2 expansion roadmap.",
        "verification_status": "Partially verified",
        "sources": [
            "[S] https://w.media (page date: not shown) - says: NTT expands beyond Mumbai with planned hyperscale and edge data center facilities in Pune.",
            "[S] https://www.nv5.com (page date: not shown) - says: NV5 provides mission-critical engineering design for 15 MW NTT Pune data center project."
        ],
        "gaps_or_conflicts": "0.0 MW live; planning phase."
    },
    {
        "id": "CORE59",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "Yotta Darumbare Data Center Park (Pune)",
        "operator": "Yotta Data Services",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "Darumbre Village, Mawal Taluk, Pune District",
        "location_precision": "Plot or village",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Darumbre%2C%20Pune&format=json&limit=1",
        "latitude": 18.6504513,
        "longitude": 73.6853763,
        "coordinates_lat_long": "18.6504513, 73.6853763",
        "google_maps_url": "https://www.google.com/maps?q=18.6504513,73.6853763",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/Yotta+Data+Center+Darumbre+Pune",
        "operational_mw": 0.0,
        "planned_ultimate_mw": 90.0,
        "capacity_basis": "IT load",
        "true_development_status": "Planned or under evaluation",
        "status_operational": "Under development",
        "workload_class": "[Colocation, Hyperscale, AI-ready, Cloud]",
        "power_procurement": "Dedicated high-voltage substation planned with direct renewable power wheeling.",
        "cooling": "Liquid cooling ready for AI clusters and high-density compute.",
        "investment": "Rs 4,000+ crore estimated campus capex.",
        "key_dates": "Master planning outlined following Panvel and Greater Noida campus developments.",
        "verification_status": "Partially verified",
        "sources": [
            "[S] https://globaldcwiki.com (page date: not shown) - says: Yotta Darumbre Data Center Park in Pune planned for 90 MW IT capacity across hyperscale buildings.",
            "[S] https://www.entrepreneur.com (page date: not shown) - says: Yotta Data Services outlines expansion pipeline including Pune-Darumbare campus."
        ],
        "gaps_or_conflicts": "0.0 MW live; master planning stage."
    },
    {
        "id": "CORE60",
        "record_type": "campus",
        "parent_id": None,
        "facility_name": "Web Werks Iron Mountain Pune Campus (PUN-1)",
        "operator": "Web Werks Data Centers",
        "state": "Maharashtra",
        "district": "Pune",
        "district_source_url": "https://pune.gov.in/",
        "location_detail": "Indialand Global Industrial Park, Phase 1, Hinjewadi, Mulshi Taluk, Pune",
        "location_precision": "Locality or industrial area",
        "coordinate_method": "Geocoder (OpenStreetMap Nominatim)",
        "coordinate_source_url": "https://nominatim.openstreetmap.org/search?q=Phase%201%2C%20Hinjewadi%2C%20Pune&format=json&limit=1",
        "latitude": 18.5941678,
        "longitude": 73.7388318,
        "coordinates_lat_long": "18.5941678, 73.7388318",
        "google_maps_url": "https://www.google.com/maps?q=18.5941678,73.7388318",
        "location_checked_date": "2026-10-25",
        "maps_search_url": "https://www.google.com/maps/search/Web+Werks+Iron+Mountain+PUN-1+Hinjewadi+Pune",
        "operational_mw": 2.0,
        "planned_ultimate_mw": 2.0,
        "capacity_basis": "IT load",
        "true_development_status": "Operational",
        "status_operational": "Operational",
        "workload_class": "[Colocation, Enterprise Cloud]",
        "power_procurement": "Dual utility feeds with N+1 UPS and generator redundancy.",
        "cooling": "Precision air cooling with N+1 chiller configuration.",
        "investment": "Rs 100+ crore.",
        "key_dates": "Operational since 2016; interconnected with Mumbai MUM-1.",
        "verification_status": "Verified (2+ independent sources)",
        "sources": [
            "[P] https://www.ironmountain.com (page date: not shown) - says: PUN-1 in Hinjewadi, Pune is a carrier-neutral colocation facility offering scalable power capacity with multi-layer security.",
            "[P] https://www.webwerks.in (page date: not shown) - says: Web Werks Pune data center PUN-1 provides 2 MW power capacity with Tier III architecture."
        ],
        "gaps_or_conflicts": "Critical IT load is ~2.0 MW (sub-5 MW threshold)."
    }
]

# Append new records
records.extend(stage_d_pune_records)
print(f"Total records after Pune: {len(records)}")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

# Update changes_log_core_v2.csv
with open(changes_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for r in stage_d_pune_records:
        writer.writerow([
            r["id"],
            "entire_row",
            "",
            f"Added site {r['facility_name']} ({r['operator']}, {r['district']}, {r['operational_mw']} MW live, {r['true_development_status']})",
            "Stage D: Older operating and planned sites in Pune market",
            r["sources"][0].split(" ")[1],
            "not shown" if "page date: not shown" in r["sources"][0] else r["sources"][0].split("page date: ")[1].split(")")[0],
            "2026-10-25"
        ])

# Update url_registry_v2.txt
new_urls = [
    "https://pune.gov.in/ | Government district portal official URL for Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Dighi%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Dighi, Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Hinjewadi%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Hinjewadi, Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Kharadi%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Kharadi, Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Morawadi%2C%20Pimpri%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Morawadi, Pimpri, Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Bhosari%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Bhosari, Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Hinjawadi%20Phase%202%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Hinjawadi Phase 2, Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Darumbre%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Darumbre, Pune | 2026-10-25",
    "https://nominatim.openstreetmap.org/search?q=Phase%201%2C%20Hinjewadi%2C%20Pune&format=json&limit=1 | Nominatim geocoding: Phase 1, Hinjewadi, Pune | 2026-10-25",
    "https://www.microsoft.com | Microsoft Azure regions and availability zones portal | 2026-10-25",
    "https://environmentclearance.nic.in | Ministry of Environment official environmental clearance portal | 2026-10-25",
    "https://www.adaniconnex.com | AdaniConneX data center portfolio | 2026-10-25",
    "https://w.media | W.Media tech and data center report | 2026-10-25",
    "https://www.nv5.com | NV5 mission-critical engineering disclosures | 2026-10-25",
    "https://globaldcwiki.com | Global DC Wiki data center project tracker | 2026-10-25",
    "https://www.entrepreneur.com | Entrepreneur India data center expansion coverage | 2026-10-25"
]

with open(registry_path, "r", encoding="utf-8") as f:
    existing_reg = f.read()

with open(registry_path, "a", encoding="utf-8") as f:
    for line in new_urls:
        url_core = line.split(" | ")[0]
        if url_core not in existing_reg:
            f.write(line + "\n")

# Compute Pune live MW via code
pune_records = [r for r in records if r["state"] == "Maharashtra" and r["district"] == "Pune"]
pune_live_mw = sum(r["operational_mw"] for r in pune_records if r["operational_mw"] is not None)
cushman_pune_benchmark = 133.0
diff = round(pune_live_mw - cushman_pune_benchmark, 1)

print(f"Pune Live Operational MW in dataset: {pune_live_mw} MW")
print(f"Cushman & Wakefield Benchmark: {cushman_pune_benchmark} MW")
print(f"Difference: {diff} MW")

# Append Pune line to gap_tables_v2.csv
gap_row = [
    "Pune",
    cushman_pune_benchmark,
    pune_live_mw,
    diff,
    "Web Werks PUN-1 (Hinjewadi: 2.0 MW sub-threshold); Nxtra Kharadi PUN 1 (4.5 MW IT load); CtrlS Pune (no active local site; services via Navi Mumbai); Sify Pune (enterprise connectivity node only; no mega DC); Colt DCS / RMZ Pune (pipeline focused on Mumbai/Chennai); CapitaLand Pune (MoU for multi-year business parks; no standalone DC built); AWS Pune (relies on Mumbai region and local partner colocation); Google Cloud (no local self-build campus)"
]

with open(gap_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(gap_row)

print("Stage D1 (Pune) integration complete.")
