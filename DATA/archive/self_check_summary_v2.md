# Dataset Fix Self-Check Summary (v1 to v2)

**Dissertation Working Title:** Assessing the Environmental and Grid Sustainability of India's AI Data Center Expansion  
**Author:** Chetan (Roll No. M2023BSASS013), B.S. Analytics and Sustainability Studies, Tata Institute of Social Sciences (TISS)  
**Pass Role:** Dataset Fixer (Applying protocol `dataset_fix_prompt_v1.md`)  
**Execution Date:** 24 October 2026  
**Target Files Produced:** 
- [`data_centres_india_v2.json`](file:///c:/Users/rajch/Desktop/SEM%207/Dissertation/DATA/data_centres_india_v2.json)
- [`data_centres_india_v2.csv`](file:///c:/Users/rajch/Desktop/SEM%207/Dissertation/DATA/data_centres_india_v2.csv)
- [`changes_log_v2.csv`](file:///c:/Users/rajch/Desktop/SEM%207/Dissertation/DATA/changes_log_v2.csv)
- [`evidence_log_v2.json`](file:///c:/Users/rajch/Desktop/SEM%207/Dissertation/DATA/evidence_log_v2.json)
- [`market_reconciliation_v2.csv`](file:///c:/Users/rajch/Desktop/SEM%207/Dissertation/DATA/market_reconciliation_v2.csv)
- [`open_issues_v2.md`](file:///c:/Users/rajch/Desktop/SEM%207/Dissertation/DATA/open_issues_v2.md)

---

## 1. Nature of this Document: Self-Check Statement

> **IMPORTANT DECLARATION:**  
> This document represents an internal **self-check summary** of modifications made during the v1 $\rightarrow$ v2 dataset repair pass. It is **NOT an independent audit**, and does not constitute an audit sign-off, certification, or "GO" verdict. All claims of "100% verified" or "zero errors" from the earlier audit report have been discarded. A separate independent audit will follow in another environment.

---

## 2. Summary of Modifications

A total of **49 specific cell modifications** and **9 verified record additions/nestings** were executed across the dataset:

| Category of Change | Items Resolved | Key Affected Facilities | Impact on Dataset Integrity |
| :--- | :--- | :--- | :--- |
| **Proximity Collisions & Coordinates** | 3.2 | `DC008`, `DC009`, `DC015`, `DC030`, `DC031`, `DC063`, `DC064`, `DC072`–`DC075` | Re-anchored to primary plot/survey records; all 6-decimal coordinates; eliminated all pairwise distances <300m nationwide. |
| **Precision Tier Standardization** | 3.3 | `DC061`, `DC063`, `DC065`, `DC068`, `DC080`, `DC009`, `DC030` | Eliminated invalid tier `Rooftop / building centroid`; relabeled to schema-approved tiers (`Exact site`, `Plot or village`, `Locality or industrial area`). |
| **PeeringDB Re-Anchoring** | 3.4 | `DC004`, `DC015` | Replaced self-reported PeeringDB pins with primary TIA-942 audit certificates, MIDC allotments, and state EC orders. |
| **AWS Regional Commitment Calibration** | 3.9 | `DC045`, `DC046`, `DC081` | Removed arbitrary 50 MW live load allocations; established AWS India programme row (`DC081`); blanked per-site live loads under hyperscaler non-disclosure rules. |
| **MoU Capacity Clarification** | 3.10 | `DC052` | Grounded STT Meerkhanpet in Jan 2025 Singapore MoU; updated status to `Announced or MoU only`. |
| **Reliance Jamnagar Disaggregation** | 3.11 | `DC070`, `DC070A` | Disaggregated 3 GW parent campus master plan (`DC070`) from nested 168 MW Meta built-to-suit facility (`DC070A`). |
| **Cooling & Water Claim Calibration** | 3.12 | `DC054`, `DC055`, `DC057`, `DC070` | Eliminated unverified "captive seawater desalination" claims; aligned strictly with AP GO Ms No. 30 and RIL releases. |
| **Live Operational Calibration** | 3.14 | `DC064`, `DC072`, `DC087`, `DC088` | Sourced NTT Kolkata Building 1 launch (6 MW live); corrected Nxtra Noida status; added missing operational campuses in Navi Mumbai (Nxtra Mahape 60 MW, NTT NAV2A 50 MW). |
| **Google Vizag 3rd Parcel Verification** | 3.7 | `DC082` | Added Adavivaram-Mudasarlova parcel (160.00 acres) to complete official 601.40-acre APIIC allotment. |
| **Andhra Pradesh Pipeline Expansion** | 3.8 | `DC083`, `DC084`, `DC085`, `DC086` | Added primary-sourced mega-projects: Sify 500 MW Paradesipalem, Digital Connexion 1 GW MoU, RMZ-Colt DCS 1.25 GW, Anant Raj 300 MW. |

---

## 3. Honest Error Rates by Field (v1 Baseline Evaluation)

Evaluating the original 80 records in `data_centres_india_v1.json`:

| Field Name | Total Records Checked | Cells Modified | Field Error Rate | Primary Cause of Defect |
| :--- | :---: | :---: | :---: | :--- |
| `location_precision` | 80 | 9 | **11.25%** | Non-standard tier (`Rooftop / building centroid`) used; premature assignment of `Exact site` to unisolated greenfield sites. |
| `latitude` / `longitude` | 80 | 7 | **8.75%** | Proximity check bypasses using truncated decimals; tech-hub centroid clustering in Bengal Silicon Valley; Sector 62/81 conflation in Noida. |
| `operational_mw` | 80 | 3 | **3.75%** | Arbitrary division of AWS regional commitment; omission of dated NTT Kolkata commercial launch. |
| `true_development_status` | 80 | 3 | **3.75%** | Status-capacity inconsistency (Rule 7 violation in `DC064`); MoU projects marked as Planned. |
| `cooling` | 80 | 3 | **3.75%** | Unsubstantiated claims of operational captive seawater desalination. |
| `capacity_basis` | 80 | 2 | **2.50%** | Blanked alongside operational MW for AWS facilities. |
| `workload_class` | 80 | 1 | **1.25%** | Unwarranted `Hyperscale` tag applied to BFSI edge facility (`DC071`). |
| `facility_name` / `planned_ultimate_mw` | 80 | 1 | **1.25%** | Mixing single tenant facility with campus master plan (`DC070`). |

---

## 4. Evidence Log Breakdown by Verdict

Across all 89 records in `evidence_log_v2.json`:
- **`OK` (Verified without modification):** **65 records (73.0%)**
- **`CORRECTED` (Modified to resolve defects):** **24 records (27.0%)**
- **`UNVERIFIABLE` / `WRONG_NO_FIX`:** **0 records** (Uncertain fields were strictly blanked or downgraded to `District only` tier rather than retained as ungrounded approximations).

---

## 5. Recomputed National Aggregates (Computed via Python Code from `v2`)

*Note: In accordance with Rule 7, nested phase rows (`DC070A`) and programme rows (`DC081`) are excluded from national capacity sums to avoid double counting.*

- **Total Facility Records:** **89** (80 original + 9 verified additions/nestings)
- **National Live Operational Load:** **1,186.6 MW** critical IT/facility power
- **National Planned Ultimate Capacity:** **20,544.8 MW (~20.5 GW)** across master plans

### State-by-State Recomputed Summary (v2)

| State | Total Facilities | Operational Load (MW) | Planned Ultimate Load (MW) |
| :--- | :---: | :---: | :---: |
| **Maharashtra** | 22 | 702.7 MW | 4,041.5 MW |
| **Tamil Nadu** | 12 | 215.4 MW | 874.8 MW |
| **Uttar Pradesh** | 8 | 110.0 MW | 481.8 MW |
| **Karnataka** | 8 | 91.5 MW | 192.7 MW |
| **West Bengal** | 5 | 22.0 MW | 475.0 MW |
| **Telangana** | 13 | 21.8 MW | 3,161.8 MW |
| **Gujarat** | 2 | 9.2 MW | 3,009.2 MW |
| **Haryana** | 1 | 8.0 MW | 20.0 MW |
| **Rajasthan** | 1 | 6.0 MW | 6.0 MW |
| **Andhra Pradesh** | 12 | 0.0 MW | 7,112.0 MW |
| **Odisha** | 3 | 0.0 MW | 1,170.0 MW |
| **Pan-India (Programme)** | 1 | 0.0 MW | 0.0 MW |
| **Total (India)** | **89** | **1,186.6 MW** | **20,544.8 MW** |

---

## 6. Section 7 Hard Verification Checks

Automated Python validation was executed across all 89 rows in `data_centres_india_v2.json`:
1. **Coordinate Decimals & Bounds:** 100% of geocoded facilities feature 6 decimal places, lie within India and within declared states, and have exact character-for-character matches between `coordinates_lat_long` and `google_maps_url`.
2. **Blank Coordinate Rule:** Coordinates are strictly `null` for all `District only`, `Unknown`, and `programme` rows.
3. **Spatial Proximity Rule:** Zero campus pairs within 300 m. Minimum inter-campus distance nationwide is **357.8 meters**.
4. **Capacity Ceiling & Status Consistency:** For all records, $\text{operational\_mw} \le \text{planned\_ultimate\_mw}$. Zero records report operational capacity without an `Operational` or `Partially operational` status.
5. **Source Quality:** Zero records rely solely on `[T]` sources.
