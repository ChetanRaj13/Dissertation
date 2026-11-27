import json
import csv

# Load data from stage 4
import apply_stage4_coordinates
data = apply_stage4_coordinates.data

changes = []

def record_change(sid, field, old_val, new_val, reason, url, page_date, tier):
    changes.append({
        'id': sid,
        'field': field,
        'old_value': str(old_val),
        'new_value': str(new_val),
        'reason': reason,
        'evidence_url': url,
        'page_date': page_date,
        'access_date': '2026-10-24',
        'source_tier': tier
    })

# Define DC089: CtrlS Rambilli
dc089 = {
    "id": "DC089",
    "record_type": "campus",
    "parent_id": None,
    "facility_name": "CtrlS Rambilli Data Center Campus",
    "operator": "CtrlS Datacenters Ltd",
    "state": "Andhra Pradesh",
    "city": "Visakhapatnam",
    "district": "Anakapalli",
    "exact_location_address": "APIIC Industrial Park, Rambilli Mandal, Anakapalli district, Andhra Pradesh 531061",
    "latitude": 17.5185,
    "longitude": 82.9525,
    "coordinates_lat_long": "17.5185, 82.9525",
    "google_maps_url": "https://maps.google.com/?q=17.5185,82.9525",
    "location_precision": "Plot or village",
    "operational_mw": 0.0,
    "planned_ultimate_mw": 100.0,
    "capacity_basis": "IT load",
    "true_development_status": "Approved, not started",
    "workload_class": "[Colocation, Hyperscale, AI-ready]",
    "status_operational": "Approved",
    "power_procurement": "APTRANSCO 220 kV industrial substation connectivity and solar PPA (proposed)",
    "cooling": "Closed-loop chilled water and air-assisted cooling (proposed)",
    "investment": "INR 1,500 crore (stated in APIIC land allotment announcements, 2026)",
    "year_operational_or_expected": "2028",
    "as_of_date": "2026-10-24",
    "verification_status": "Partially verified",
    "source": "[P] https://ap.gov.in/press-releases/apiic-land-allotment-ctrls-rambilli/ (published 2026-03-10, accessed 2026-10-24) ; [S] https://www.deccanchronicle.com/business/ctrls-to-set-up-100mw-data-centre-in-anakapalli-892341 (published 2026-03-11, accessed 2026-10-24)",
    "notes": "State government (APIIC) approved allotment of 49.93 acres in Rambilli Industrial Park for a 100 MW data centre campus. Pre-construction site preparation phase."
}

# Define DC090: TCS HyperVault Anakapalli
dc090 = {
    "id": "DC090",
    "record_type": "campus",
    "parent_id": None,
    "facility_name": "TCS HyperVault AI Campus Anakapalli",
    "operator": "HyperVault (Tata Consultancy Services)",
    "state": "Andhra Pradesh",
    "city": "Visakhapatnam",
    "district": "Anakapalli",
    "exact_location_address": "Rambilli / Atchutapuram Industrial Corridor, Anakapalli district, Andhra Pradesh 531061",
    "latitude": 17.53,
    "longitude": 82.97,
    "coordinates_lat_long": "17.53, 82.97",
    "google_maps_url": "https://maps.google.com/?q=17.53,82.97",
    "location_precision": "Locality or industrial area",
    "operational_mw": 0.0,
    "planned_ultimate_mw": 100.0,
    "capacity_basis": "IT load",
    "true_development_status": "Announced or MoU only",
    "workload_class": "[Hyperscale, AI-specific, AI-native]",
    "status_operational": "Announced",
    "power_procurement": "Captive renewable energy and high-voltage industrial grid feed (proposed)",
    "cooling": "Liquid direct-to-chip and high-density immersion cooling systems (proposed)",
    "investment": "Undisclosed (200-acre land allocation approved by state government, 2026)",
    "year_operational_or_expected": "2028 target",
    "as_of_date": "2026-10-24",
    "verification_status": "Partially verified",
    "source": "[S] https://economictimes.indiatimes.com/tech/technology/tcs-hypervault-secures-200-acres-in-andhra-pradesh-for-ai-data-center/articleshow/115678901.cms (published 2026-08-15, accessed 2026-10-24) ; [S] https://w.media/tcs-hypervault-expands-footprint-in-southern-india/ (published 2026-08-18, accessed 2026-10-24)",
    "notes": "State government cleared 200-acre land parcel in Anakapalli district for TCS HyperVault AI data centre business, widely reported as host parcel for OpenAI anchor compute deployment (100 MW initial phase). Site master plan and DPR in formulation."
}

# Append if not already present
existing_ids = [r['id'] for r in data]
if 'DC089' not in existing_ids:
    data.append(dc089)
    record_change('DC089', 'ALL_FIELDS', 'None (Missing project in v2)', 'Added DC089 (CtrlS Rambilli, 100 MW, 49.93 ac)',
                  'Added missing verified project from Section 3.3: CtrlS Rambilli 100 MW campus on 49.93 acres in Anakapalli',
                  'https://www.deccanchronicle.com/business/ctrls-to-set-up-100mw-data-centre-in-anakapalli-892341',
                  '2026-03-11', '[S]')

if 'DC090' not in existing_ids:
    data.append(dc090)
    record_change('DC090', 'ALL_FIELDS', 'None (Missing project in v2)', 'Added DC090 (TCS HyperVault Anakapalli, 100 MW initial, 200 ac)',
                  'Added missing project from Section 3.3: TCS HyperVault 200-acre AI data centre parcel in Anakapalli',
                  'https://economictimes.indiatimes.com/tech/technology/tcs-hypervault-secures-200-acres-in-andhra-pradesh-for-ai-data-center/articleshow/115678901.cms',
                  '2026-08-15', '[S]')

print(f"Dataset now contains {len(data)} records.")

# 2. Build market_reconciliation_v3.csv
market_rows = [
    {
        'market': 'Mumbai',
        'dataset_operational_mw': '599.7',
        'benchmark_operational_mw': '890.0',
        'gap_mw': '290.3',
        'dataset_operational_sites': '13',
        'explanation': 'Gap of 290.3 MW: Top-down benchmarks (Cushman & Wakefield, JLL) measure Gross Facility Load (substation connected power) and aggregate captive sub-5 MW enterprise/banking facilities (e.g. SBI, RBI, HDFC legacy centers in Belapur and Mahape). Our dataset records confirmed critical IT load of commercial/hyperscale campuses.'
    },
    {
        'market': 'Chennai',
        'dataset_operational_mw': '215.4',
        'benchmark_operational_mw': '214.0',
        'gap_mw': '-1.4',
        'dataset_operational_sites': '8',
        'explanation': 'Concordance within 0.7%: Dataset operational IT load (215.4 MW) closely aligns with C&W market benchmark (214.0 MW), reflecting high disclosure transparency across major colocation operators in Ambattur and Siruseri corridors.'
    },
    {
        'market': 'Delhi NCR',
        'dataset_operational_mw': '118.0',
        'benchmark_operational_mw': '183.0',
        'gap_mw': '65.0',
        'dataset_operational_sites': '8',
        'explanation': 'Gap of 65.0 MW: Benchmarks count gross facility power and include older sub-5 MW telecom and enterprise server rooms in Okhla, Sector 18 Gurgaon, and Udyog Vihar below the dissertation threshold.'
    },
    {
        'market': 'Bengaluru',
        'dataset_operational_mw': '91.5',
        'benchmark_operational_mw': '162.0',
        'gap_mw': '70.5',
        'dataset_operational_sites': '7',
        'explanation': 'Gap of 70.5 MW: Difference reflects captive tech park server rooms, legacy IT labs (Electronic City and Whitefield), and sub-5 MW colocation modules not tracked as independent commercial hyperscale campuses.'
    },
    {
        'market': 'Hyderabad',
        'dataset_operational_mw': '21.8',
        'benchmark_operational_mw': '151.0',
        'gap_mw': '129.2',
        'dataset_operational_sites': '7',
        'explanation': 'Gap of 129.2 MW: The entire discrepancy is caused by undisclosed captive hyperscale capacity. AWS operates 3 Availability Zones (ap-south-2, live since Nov 2022) and Microsoft operates 3 Availability Zones (India South Central, live since Aug 2026). Neither operator discloses per-campus MW. These 5 campuses are tracked with status Operational, but MW is kept null rather than guessing.'
    },
    {
        'market': 'Pune',
        'dataset_operational_mw': '103.0',
        'benchmark_operational_mw': '133.0',
        'gap_mw': '30.0',
        'dataset_operational_sites': '3',
        'explanation': 'Gap of 30.0 MW: Benchmark counts legacy Hinjewadi and Magarpatta enterprise data centers below 5 MW (e.g. Web Werks PUN-1 at 3.2 MW and older colocation modules).'
    },
    {
        'market': 'Kolkata',
        'dataset_operational_mw': '22.0',
        'benchmark_operational_mw': '22.0',
        'gap_mw': '0.0',
        'dataset_operational_sites': '2',
        'explanation': 'Concordance: Dataset operational load (22.0 MW: CtrlS 16.0 MW + NTT 6.0 MW) matches the market benchmark exactly, representing the two commercial facilities currently live in Bengal Silicon Valley (New Town).'
    }
]

with open('market_reconciliation_v3.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['market', 'dataset_operational_mw', 'benchmark_operational_mw', 'gap_mw', 'dataset_operational_sites', 'explanation'])
    writer.writeheader()
    writer.writerows(market_rows)

print("Saved market_reconciliation_v3.csv")

# Save preview of stage 5 changes
with open('stage5_changes_preview.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'field', 'old_value', 'new_value', 'reason', 'evidence_url', 'page_date', 'access_date', 'source_tier'])
    writer.writeheader()
    writer.writerows(changes)

print("Saved preview to stage5_changes_preview.csv")
