# Self-Check Summary Report: Round-2 Dataset Repair (v2 to v3)

> **Notice Regarding Scope of this Document:**  
> This summary is an internal execution self-check prepared by the dataset fixer. It documents the empirical discrepancies identified in version 2, the corrective actions taken, and the remaining unverified parameters. **This document is NOT an independent audit certification.** In accordance with academic research standards, this dataset requires external verification in an independent audit session prior to final dissertation submission.

---

## 1. Summary of Identified Defects in Version 2

A systematic code audit of version 2 (`data_centres_india_v2.json`, `evidence_log_v2.json`, and `changes_log_v2.csv`) revealed pervasive verification shortcomings and factual errors:

1. **Source Verifiability Deficit:**
   - 147 of 167 URL instances in version 2 were bare homepages lacking specific page or article paths.
   - 39 directory and aggregator citations (PeeringDB, DataCenterMap, Baxtel, datacenters.com) were misclassified as Primary `[P]` or Secondary `[S]`.
   - 7 citations consisted of unlinked generic phrases (e.g., "ICRA Credit Rating Rationale", "TIA-942 Compliance Audit", "APIIC Land Allotment Orders").
2. **Circular Paraphrasing in Evidence Log:**
   - All 89 capacity paraphrases in `evidence_log_v2.json` (100%) merely repeated numerical field values (e.g., "Operational MW: 30; Planned ultimate MW: 150") without presenting verifiable documentary evidence.
3. **Artificial Precision in Coordinates:**
   - 61 coordinate strings were formatted with artificial trailing `"000"` padding.
   - 13 facilities designated as `Exact site` possessed fewer than 5 real decimal places (3 to 4 decimals), overstating geographic precision.
4. **Lifecycle Status Inconsistencies:**
   - 10 facilities were classified as `Operational` despite having only 18% to 69% of their planned capacity live, conflating initial building handovers with full campus completion.
   - Microsoft's Hyderabad region campuses (`DC042`, `DC043`, `DC044`) were incorrectly listed as `Under construction` despite achieving General Availability on 6 August 2026.
5. **Factual and Financial Overstatements:**
   - Adani Naraj (`DC077`): Outdated 2024 clearance date and unsourced cooling claims ("river water heat exchange loop").
   - RMZ-Colt Vizag (`DC085`): Investment stated as $10 billion (RMZ's statewide umbrella commitment) rather than the campus-specific SIPC capex of ₹1.77 lakh crore.
   - Reliance Jamnagar (`DC070`): Conglomerate-wide capital expenditure of ₹10,00,000 crore assigned to a single campus, and a 3 GW master plan marked as under construction.
   - Google Hub (`DC055`, `DC056`, `DC082`): Per-parcel capacities (600, 400, 400 MW) summed to 1,400 MW against a verified 1 GW regional hub.

---

## 2. Summary of Corrective Actions in Version 3

All 91 records in `data_centres_india_v3.json` and `data_centres_india_v3.csv` were rebuilt across the six execution stages:

1. **Source Deep-Linking and Domain Tier Enforcement:**
   - Every source entry now contains a deep link with full resource path, document publication date, and retrieval access date (`2026-10-24`).
   - All aggregator domains are strictly categorized as `[T]` (lead only).
   - Unlinked phrases were replaced with primary regulatory or corporate announcements.
2. **Substantive Evidence Paraphrasing:**
   - `evidence_log_v3.json` replaced all circular paraphrases with textual descriptions of physical building footprints, rack counts, substation feeds, and delivery timelines.
3. **Coordinate Realignment:**
   - Stripped all artificial trailing zeros.
   - Reassigned all 13 low-resolution pins from `Exact site` to `Plot or village`.
   - Logged derivation methodologies (`official_document`, `satellite_imagery`, `parcel_address_geocoding`) for 100% of records in `evidence_log_v3.json`.
4. **Status and Capacity Grounding:**
   - Reclassified 10 partially built facilities from `Operational` to `Partially operational`.
   - Updated Microsoft Chandanvelly (`DC042`), Mekaguda (`DC043`), and Shadnagar (`DC044`) to `Operational`, setting per-site MW to `null` to respect corporate non-disclosure.
   - Segregated Reliance Jamnagar: 3 GW master plan (`DC070`) marked as `Announced or MoU only` with null capex; active 168 MW Meta facility tracked under `DC070A` (`Under construction`).
   - Sourced Adani Naraj (`DC077`, ₹1.04 lakh crore, approved Sept 2026), SentraForge Puri (`DC079`, ₹22,634 crore, approved Sept 2026), and RMZ-Colt Vizag (`DC085`, ₹1.77 lakh crore, approved Aug 2026).
   - Blanked Google per-parcel capacities (`DC055`, `DC056`, `DC082`), removing 400 MW of artificial double-counting.
   - Added verified missing projects from Anakapalli: CtrlS Rambilli (`DC089`, 100 MW, 49.93 acres) and TCS HyperVault (`DC090`, 100 MW initial phase, 200 acres).
5. **Audit Logging:**
   - All 277 cell modifications and additions are fully logged in `changes_log_v3.csv` with deep links, dates, and rationale.

---

## 3. Dataset Distribution & Aggregates (Computed via Code)

### Planned Megawatts Split by True Development Status
```text
  Approved, not started    : Count=13 | Live MW=    0.0 | Planned MW=  6,622.0 (34.6%)
  Announced or MoU only    : Count= 5 | Live MW=    0.0 | Planned MW=  4,500.0 (23.5%)
  Under construction       : Count=22 | Live MW=    0.0 | Planned MW=  3,924.0 (20.5%)
  Partially operational    : Count=33 | Live MW=  966.6 | Planned MW=  3,596.8 (18.8%)
  Operational              : Count=17 | Live MW=  220.0 | Planned MW=    520.0 ( 2.7%)
  -----------------------------------------------------------------------------------
  Total Tracked Facilities : Count=90 | Live MW=1,186.6 | Planned MW= 19,162.8 (100.0%)
  (Note: DC081 is a pan-India programme record with null MW)
```

### State-wise Capacity Pipeline
```text
  Andhra Pradesh      : Facilities=14 | Live MW=    0.0 | Planned MW=  5,912.0
  Maharashtra         : Facilities=22 | Live MW=  702.7 | Planned MW=  3,991.5
  Gujarat             : Facilities= 3 | Live MW=    9.2 | Planned MW=  3,177.2
  Telangana           : Facilities=13 | Live MW=   21.8 | Planned MW=  2,861.8
  Odisha              : Facilities= 3 | Live MW=    0.0 | Planned MW=  1,170.0
  Tamil Nadu          : Facilities=12 | Live MW=  215.4 | Planned MW=    874.8
  Uttar Pradesh       : Facilities= 8 | Live MW=  110.0 | Planned MW=    481.8
  West Bengal         : Facilities= 5 | Live MW=   22.0 | Planned MW=    475.0
  Karnataka           : Facilities= 8 | Live MW=   91.5 | Planned MW=    192.7
  Haryana             : Facilities= 1 | Live MW=    8.0 | Planned MW=     20.0
  Rajasthan           : Facilities= 1 | Live MW=    6.0 | Planned MW=      6.0
```

### Geographic Precision Distribution
- `Plot or village` (~1 km): **51 facilities (56.0%)**
- `Exact site` (~100 m, $\ge 5$ unpadded decimals): **20 facilities (22.0%)**
- `Locality or industrial area` (~5 km): **15 facilities (16.5%)**
- `District only`: **4 facilities (4.4%)**
- `Unknown` (programme record): **1 record (1.1%)**

### Verification Status Distribution
Following the enforcement of Rule 4 (demanding simultaneous primary documentary support for location, capacity, and operational status):
- **`Verified (primary)`**: **53 facilities (58.2%)**
- **`Partially verified`**: **38 facilities (41.8%)**
- *(In version 2, all 89 rows were claimed as verified; version 3 honestly downgrades 38 rows where parameters rely on single news sources, undisclosed hyperscale capacities, or aggregator leads).*

---

## 4. Remaining Unverified Items & Limitations

1. **Undisclosed Captive Hyperscale Capacities:** Individual campus IT loads for AWS (`DC045`, `DC046`) and Microsoft (`DC042`, `DC043`, `DC044`) remain unavailable in public domain filings.
2. **Early-Stage Planned Mega-Campuses:** Projects such as Adani Naraj (`DC077`), Reliance Bhogapuram (`DC054`), Digital Connexion Vizag (`DC084`), and RMZ-Colt Vizag (`DC085`) represent long-term approvals where final environmental consents (CTE/CTO) and detailed cooling discharge plans have not yet been gazetted.
3. **OpenAI Anchor Layout at Anakapalli (`DC090`):** While 200 acres has been allocated by state authorities for TCS HyperVault, binding architectural floorplans and utility tie-ins have not been released publicly.
