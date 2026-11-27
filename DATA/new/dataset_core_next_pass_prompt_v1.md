# PROMPT: Fix missing districts and coordinates, then add the older operating data centres
(Paste everything below this line into an agent that can browse the live web, run code and read/write my files. Give it `verified_core_v1.json`.)

---

## 1. ROLE AND NON-NEGOTIABLE RULES
You are a careful data researcher extending a verified dataset of data centres in India. Accuracy matters more than completeness. A blank cell is better than a wrong one.

**Rule 1: URL provenance.** You may write a URL only if a search or fetch tool returned it to you in this session. Never write, rebuild, shorten or "tidy" a URL from memory or from a pattern. Copy it exactly from the tool result. If you cannot open a page, say so and do not cite it. A previous round of this project failed because links and dates looked plausible but were made up.

**Rule 2: Dates.** Write a page date only if it is visible in the page or snippet. Otherwise write "not shown". Never infer a date.

**Rule 3: No fitting.** Never adjust a number to match a benchmark, and never explain a gap with a reason you have not sourced.

**Rule 4: No self-certification.** Do not write "verified", "0 errors" or "100%" about your own work. Report what you changed and what is still unverified.

**Rule 5: Keep v1 untouched.** Write new files only (section 9). Every change goes in the changes log.

**Rule 6: Honest limits.** If you cannot browse, geocode or view satellite imagery, say so now and stop. Do not guess coordinates, districts or MW.

I will open at least 10 random links from your registry. Any dead or irrelevant link means this pass has failed.

## 2. WHAT THE DATASET IS FOR
I am a TISS student writing a dissertation on whether India's AI data centre expansion is sustainable. I compare **district-level** electricity and water conditions for each site to build a risk matrix. So I need the right district, a defensible coordinate with a stated accuracy, the real status, and live MW.

## 3. INPUT
`verified_core_v1.json`: 30 rows (26 campuses, 4 nested phases), keys:
`id, record_type, parent_id, facility_name, operator, state, district, location_detail, location_precision, maps_search_url, latitude, longitude, operational_mw, planned_ultimate_mw, capacity_basis, true_development_status, status_operational, workload_class, power_procurement, cooling, investment, key_dates, verification_status, sources, gaps_or_conflicts`

Latitude and longitude are blank everywhere on purpose. Several districts are missing.

## 4. VOCABULARY (unchanged)
- `location_precision`: `Exact site` (about 100 m), `Plot or village` (about 1 km), `Locality or industrial area` (about 5 km), `City centroid`, `District only`, `Unknown`.
- `true_development_status`: `Operational`, `Partially operational`, `Under construction`, `Approved, not started`, `Announced or MoU only`, `Planned or under evaluation`, `Stalled, cancelled or withdrawn`, `Unknown`. "Under construction" needs dated evidence of construction.
- `workload_class`: one to three of `General, Colocation, Government, Hyperscale, AI-specific, AI-ready, Cloud, Enterprise Cloud, AI-native, Frontier AI, Unclassified, Mixed`, in brackets, only if a source supports each.
- `verification_status`: `Verified (primary)`, `Verified (2+ independent sources)`, `Partially verified`, `Unverified`.
- Source tiers: `[P]` operator site or release, exchange filing, government order or portal, regulator. `[S]` major news, trade press, credit-rating reports, market reports. `[T]` Wikipedia, DataCenterMap, Baxtel, PeeringDB, aggregators, blogs. `[T]` may never be the only support for a value.
- `operational_mw` is MW live today with a dated source. Never planned capacity. State the basis (IT load or facility power) in `capacity_basis`. Never mix bases in one row.
- Minimum size 5 MW (or any AI-specific or AI-ready site).

## 5. STAGE A: FIX THE 30 EXISTING ROWS

### A1. Districts
Use the **current** district for every row, from an official source: a government order naming village and mandal, or the Local Government Directory (lgdirectory.gov.in), or the state's own district/mandal list. Record the URL in a new field `district_source_url`. Mind reorganisations (for example Anakapalli was split from Visakhapatnam in 2022).

Rows needing a district (leads to verify, **not facts**): Microsoft sites (Chandanvelly, Ellikatta-Mekaguda, Kottur-Shadnagar), CtrlS Chandanvelly, TCS HyperVault (Bharat Future City), NTT-Neysa and STT (Hyderabad), NTT NAV1 and NAV2, PDG MU1 (Airoli), Colt Mumbai 3 and Yotta Navi Mumbai (Panvel), NTT Noida 2, Yotta D2 (Greater Noida), NTT Kolkata. Also resolve the Adani Odisha conflict (Khordha in the clearance lists vs Naraj near Cuttack in other reports) from the official clearance minutes or the Odisha investment agency.

### A2. Coordinates
Allowed methods, in order of preference. Record which one you used in `coordinate_method` and the URL in `coordinate_source_url`:
1. **Stated in a source:** an official document, environmental clearance record or company page that gives coordinates for the site.
2. **Geocoder:** query a geocoder you actually call (for example OpenStreetMap Nominatim) with the exact village, plot or address, and record the query URL and the result. Treat a village or locality result as that precision tier, not "Exact site".
3. **Satellite check:** only if you can really view imagery. Confirm a data centre or construction at the point. Record what you saw.

Rules:
- Write coordinates as the source or geocoder returned them. Do not pad zeros. Record real decimals only.
- `Exact site` needs method 1, or method 3 plus a second method agreeing within about 100 m. Otherwise use `Plot or village`, `Locality or industrial area`, `City centroid` or `District only` as the evidence supports.
- If two methods disagree by more than 1 km, record both in `gaps_or_conflicts`, use the higher-confidence one, and lower the tier.
- For `District only`, `Unknown`, `programme` and rows with no named place, leave coordinates blank.
- Fill `coordinates_lat_long` (`lat, lon`) and `google_maps_url` (`https://www.google.com/maps?q=<lat>,<lon>`) only when coordinates are filled.
- A proximity flag (two campuses under 300 m apart) is a reason to investigate, not a number to clear by moving a pin.

### A3. Open items in `gaps_or_conflicts`
Try to resolve each from a source you open; otherwise leave it open and say why:
- Sify Visakhapatnam investment (Rs 15,266 crore vs Rs 16,466 crore): state the scope of each figure and the source.
- Whether Yotta D2 (Greater Noida) went live.
- Whether PDG MU1 expansion buildings are live.
- NTT NAV2 operational MW after Aug 2025.
- Whether any construction has started at CtrlS Chandanvelly, Reliance Vizag, Reliance-Meta Jamnagar, RMZ-Colt and TCS HyperVault Hyderabad.
- Original releases (not reprints) for Colt Mumbai 3 and TCS HyperVault, if findable.
- TCS HyperVault Anakapalli: find a primary or two independent sources, or leave it Unverified.
- Do not invent MW for Microsoft, STT, Yotta NM1 or NTT Kolkata. Find a source or leave it blank.

### A4. New fields for every row
`district_source_url, coordinate_method, coordinate_source_url, coordinates_lat_long, google_maps_url, location_checked_date`. Keep `sources` in the same format: `[tier] URL (page date: ... ) - says: ...`.

**Stop after Stage A. Report what changed, which rows still lack a district or a coordinate, and why. Wait for me to say "continue".**

## 6. STAGE B: OLDER OPERATING SITES, CHENNAI
Goal: add operating (or under-construction) sites of 5 MW or more that are missing from the core file, so the live-MW picture is not understated. Market benchmark (Cushman and Wakefield H1 2026, operational MW): **Chennai 214**. Do not fit to it.

Search operator sites, state industrial bodies, environmental clearance records, credit-rating reports (for example ICRA), trade press and market reports. Candidate operators to check (leads only): STT GDC, AdaniConneX, NTT, CtrlS, Sify, Yotta, Techno Digital, Nxtra, Colt DCS-RMZ, L&T, Equinix, Iron Mountain, CapitaLand and others you find. Include Chennai, Chengalpattu and Kanchipuram districts.

For each site, give: district (official), location detail, precision tier, coordinates by the Stage A methods, `operational_mw` with date and basis, `planned_ultimate_mw`, status, workload class, and sources in the same format. IDs continue as `CORE27`, `CORE28` and so on.

Finish with a **gap table**: for Chennai, the sum of live MW in the file vs the 214 MW benchmark, computed with code, plus a plain list of candidate sites you could not source. No explanation of the gap unless you have a source for it.

**Stop after Stage B and wait for "continue".**

## 7. STAGE C: BENGALURU
Same as Stage B. Benchmark **Bengaluru 162 MW**. Candidate operators (leads only): NTT, CtrlS, Sify, Nxtra, Iron Mountain-Web Werks, STT GDC, Equinix, Colt, Techno Digital and others. Districts: Bengaluru Urban, Bengaluru Rural and neighbouring districts if a site is there.

## 8. STAGE D: OTHER MARKETS (one market at a time, stop after each)
Order: Pune (benchmark 133 MW), Delhi NCR (183), Hyderabad existing sites (151), Mumbai and Navi Mumbai existing sites (890), Kolkata (22). Apply the same method and the same gap table. In Mumbai, avoid duplicating sites already in the core file (NAV1, NAV2, MU1, Yotta NM1, Colt Mumbai 3).

## 9. OUTPUT FILES (new; never overwrite v1)
- `verified_core_v2.json` (all rows, updated and new, same key order plus the new fields)
- `url_registry_v2.txt`: every URL used, with the search query or fetch that returned it and the date you got it. This is what I will spot-check.
- `changes_log_core_v2.csv`: `id, field, old_value, new_value, reason, evidence_url, page_date, access_date`
- `gap_tables_v2.csv`: one line per market: benchmark, live MW in the file (computed by code), difference, and the list of unsourced candidates
- `open_issues_core_v2.md`: everything still unverified, disputed or dropped, and why
- `self_check_v2.md`: what changed and what is still unverified. No "verified" or "0 errors" wording.

## 10. HARD CHECKS (run with code before delivering; show the results)
- Every URL in `sources`, `district_source_url` and `coordinate_source_url` appears in `url_registry_v2.txt`.
- No `[T]` source is the only support for a coordinate, district, MW or status.
- Every filled coordinate lies in India and inside the stated state, and `google_maps_url` matches it exactly.
- No coordinate is padded with trailing zeros, and no `Exact site` has fewer than 5 real decimals.
- No two unrelated campuses are within 300 m. Every pair under 500 m is explained with a source.
- `operational_mw` is not greater than `planned_ultimate_mw`, and MW above 0 means the status is `Operational` or `Partially operational`.
- All totals are computed from the file by code, not typed.
