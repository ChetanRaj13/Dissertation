# Open Issues, Disputed Points, and Verification Gaps (v2)

**Dissertation Project:** Assessing the Environmental and Grid Sustainability of India's AI Data Center Expansion  
**Author:** Chetan (Roll No. M2023BSASS013), TISS  
**Dataset Version:** `v2` (Derived from review of v1 and independent web cross-checks)  
**Date:** 24 October 2026  

---

## 1. Executive Summary of Open Issues

In accordance with Section 1 of the dataset fix protocol ("Accuracy matters more than completeness; a blank cell is better than a wrong one"), this document records all parameters that could not be independently corroborated with primary regulatory evidence. These items remain explicitly blanked, downgraded, or marked for follow-up in the upcoming independent audit.

---

## 2. Hyperscale Operator Non-Disclosure Gaps

### 2.1 Amazon Web Services (AWS) Availability Zones (`DC045`, `DC046`)
- **Issue:** Commercial market reports (e.g., Cushman & Wakefield, JLL) attribute an estimated 100–120 MW of operational load to AWS in Hyderabad. However, AWS does not publish per-site critical IT loads or facility power ratings for its Availability Zones.
- **Resolution in v2:** The arbitrary 50 MW split in each of `DC045` (Chandanvelly) and `DC046` (Fab City) was removed. `operational_mw` and `capacity_basis` are set to `null` (blank).
- **Follow-up Needed:** Monitor Telangana State Pollution Control Board (TSPCB) Consent to Operate (CTO) filings or DISCOM tariff petitions (TSSPDCL) for dedicated contract maximum demand (CMD) allocations in MVA.

### 2.2 Microsoft Azure India Central / South Central Availability Zones (`DC042`, `DC043`, `DC044`)
- **Issue:** Microsoft Hyderabad cloud region became generally available in August 2026 and formally opened on 24 September 2026. While cadastral boundary coordinates are derived directly from SEIAA environmental clearance benchmarks (e.g., Mekaguda and Chandanvelly), live operating IT load is withheld.
- **Resolution in v2:** `operational_mw` is set to `null` (blank); `true_development_status` is verified as `Operational` (Chandanvelly HYD11) and `Under construction` (Mekaguda HYD01, Shadnagar HYD04).

---

## 3. Water Intake and Cooling Clearances in Coastal Mega-Campuses

### 3.1 Reliance Giga-Scale AI Cluster, Vizianagaram (`DC054`)
- **Issue:** Earlier reports claimed "captive seawater desalination".
- **Primary Reality:** Andhra Pradesh Government Order Ms No. 30 (20 May 2026) allots 854.97 acres and grants water tariff concessions, but the physical intake source (e.g., deep aquifer borewells vs. municipal supply vs. coastal pipeline) has not been confirmed in public environmental impact assessments.
- **Resolution in v2:** Cooling description calibrated to: `Water-cooled chiller system proposed; state water tariff subsidy granted (AP GO Ms No. 30); specific water source not confirmed / not disclosed`.

### 3.2 Google Cloud AI Hub, Visakhapatnam & Anakapalli (`DC055`, `DC056`, `DC082`)
- **Issue:** Seawater cooling was reported as active/confirmed.
- **Primary Reality:** Seawater cooling is proposed in the conceptual master plan for the 601.40-acre multi-campus cluster (Adani Infra / Raiden Infotech), but Coastal Regulation Zone (CRZ) clearances from MOEFCC for marine intake and brine discharge pipelines have not been notified.
- **Resolution in v2:** Sourced cooling description updated to: `Direct liquid-to-chip and closed-loop evaporative cooling; seawater cooling proposed in conceptual master plan; not yet commissioned`.

---

## 4. Cadastral Precision Gaps for Early-Stage MoUs (Andhra Pradesh)

### 4.1 Digital Connexion Vizag 1 GW Campus (`DC084`) & Anant Raj Cloud Vizag (`DC086`)
- **Issue:** Both entities signed high-profile MoUs with the Government of Andhra Pradesh (APEDB and IT Minister Nara Lokesh) for 1,000 MW and 300 MW respectively.
- **Limitation:** As of October 2026, specific survey numbers and village parcels have not been gazetted by APIIC.
- **Resolution in v2:** `latitude`, `longitude`, `coordinates_lat_long`, and `google_maps_url` remain strictly blank (`null`). Precision tier is set to `District only`.

---

## 5. Sub-5 MW Facilities Excluded by Protocol Cutoff

A discrepancy of ~400 MW between commercial real estate benchmarks and our dataset is driven by sub-5 MW legacy or enterprise installations. The following verified operating facilities were evaluated and intentionally excluded from `v2`:

1. **Web Werks / Iron Mountain PUN-1 (Hinjewadi, Pune):** 3.2 MW IT capacity.
2. **NTT Netmagic BLR 2 (Electronic City, Bengaluru):** 4.5 MW IT capacity.
3. **Web Werks / Iron Mountain MUM-1 (Rabale, Navi Mumbai):** 2.3–4.0 MW IT capacity.
4. **Sify Technologies Ambattur 01 (Chennai):** 3.5 MW legacy banking colocation.
5. **National / State Supercomputers (C-DAC AIRAWAT, PARAM Ananta, PARAM Siddhi):** Excluded as academic/sovereign HPC nodes without commercial cloud/colocation services.
