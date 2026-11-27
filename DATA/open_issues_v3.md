# Open Issues & Research Backlog (v3 Dataset)

This document records unresolved empirical questions, missing data points, and ongoing monitoring targets identified during the Round-2 repair of the India data centre dataset (`data_centres_india_v3.json`). It is prepared for academic tracking in the dissertation risk matrix.

---

## 1. Undisclosed Captive Hyperscale Megawatt Capacities

Several major hyperscale cloud operators maintain a strict corporate policy against disclosing individual campus or per-Availability Zone (AZ) power ratings. Rather than introducing speculative or rounded figures, these cells are deliberately maintained as `null`:

1. **Amazon Web Services (AWS) Asia Pacific (ap-south-2) Region:**
   - **Campuses:** Chandanvelly (`DC045`), Fab City (`DC046`), and third planned AZ (Pharma City).
   - **Issue:** All campuses are operational (live since November 2022), but individual building electrical capacity is undisclosed by AWS.
   - **Research Action:** Monitor state distribution company (TSSPDCL) open-access filings and dedicated 220/33 kV substation sanction orders for physical transformer ratings to infer upper grid bounds.

2. **Microsoft India South Central Region:**
   - **Campuses:** Chandanvelly HYD11 (`DC042`), Mekaguda HYD01 (`DC043`), and Shadnagar HYD04 (`DC044`).
   - **Issue:** Achieved General Availability on 6 August 2026. Microsoft does not publicly report per-site IT megawatt loads.
   - **Research Action:** Examine environmental clearance (SEIAA Telangana) filings and state electricity regulatory commission (TSERC) grid inter-connection agreements for sanctioned MVA limits.

---

## 2. Megawatt Allocations for Multi-Parcel Hubs

1. **Google Cloud AI Hub (Visakhapatnam Corridor, Andhra Pradesh):**
   - **Campuses:** Tarluvada (`DC055`), Rambilli (`DC056`), and Adavivaram-Mudasarlova (`DC082`).
   - **Issue:** Total state government clearance confirms a 1 GW (1,000 MW) aggregate investment across 601.4 acres. Individual parcel MW figures reported in earlier news articles (600 MW, 400 MW, 400 MW = 1,400 MW) were ungrounded and double-counted capacity.
   - **Status in v3:** Per-parcel MW figures are blanked (`null`) pending detailed engineering DPR submissions by Raiden Infotech / Adani Infra.

---

## 3. High-Capacity Approvals Under Pre-Construction Development

1. **Adani High Density Naraj Giga Park, Cuttack (`DC077`):**
   - **Issue:** Cleared at the 46th Odisha HLCA meeting in September 2026 for a 1 GW capacity on ~250 acres with ₹1.04 lakh crore investment. Unsourced claims in earlier drafts regarding "river water heat exchange loop" from Mahanadi and specific OPTCL sub-station tie-ins were purged.
   - **Research Action:** Track formal Detailed Project Report (DPR) and State Pollution Control Board (OSPCB) Consent to Establish (CTE) for water consumption and cooling tower discharge specifications.

2. **SentraForge AI Sovereign Campus, Puri (`DC079`):**
   - **Issue:** 120 MW sovereign compute project backed by GVPR Engineers cleared in September 2026 (₹22,634 crore). Exact village parcel coordinates are pending cadastral land demarcation by IDCO.
   - **Research Action:** Monitor IDCO parcel lease deeds for precise survey numbers and GIS boundaries.

3. **TCS HyperVault AI Campus, Anakapalli (`DC090`):**
   - **Issue:** 200 acres allotted by the Andhra Pradesh government. Widely reported as the anchor site for OpenAI's 100 MW India compute deployment, but commercial agreements and building layouts are not yet registered in public regulatory filings.
   - **Status in v3:** Tracked as `Announced or MoU only` with `Locality or industrial area` coordinate resolution.

---

## 4. Sub-5.0 MW Cutoff Policy Exceptions

Two facilities with operational phases below the dissertation's 5.0 MW cutoff have been retained under documented exceptions:
1. **DC040 (Web Werks Iron Mountain BLR-1, Bengaluru):** Operational at 4.1 MW critical IT load, but total planned campus capacity is 7.5 MW.
2. **DC064 (Airtel Nxtra Noida NCR III, Noida):** Operational at 4.5 MW critical IT load, with total planned campus capacity of 8.5 MW.
- **Protocol Justification:** Both campuses exceed 5.0 MW on a master-plan basis and house active AI-ready enterprise infrastructure. Their initial live phases are documented as `Partially operational` rather than excluded.

---

## 5. Ongoing Monitoring Targets for Dissertation Risk Matrix

- **Water Stress Cross-Referencing:** Visakhapatnam and Anakapalli campuses (`DC055`, `DC056`, `DC057`, `DC058`, `DC059`, `DC060`, `DC082`, `DC083`, `DC084`, `DC085`, `DC086`, `DC089`, `DC090`) require close evaluation against the Mudasarlova reservoir and local groundwater depletion metrics.
- **Grid Stability in Ranga Reddy District, Telangana:** Concentration of hyperscale campuses in Chandanvelly (`DC041`, `DC042`, `DC045`, `DC050`) poses localized peak transmission stress on TSSPDCL 400/220 kV substations.
