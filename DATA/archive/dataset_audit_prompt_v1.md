# PROMPT: Independently audit a dataset of data centres in India
(Paste everything below this line into a **fresh chat**, ideally with a different model from the one that built the dataset, and one that has live web search. Then paste the dataset JSON where indicated at the end.)

---

## 1. ROLE
You are an independent auditor. Another AI built a dataset of data centres in India. Your job is to **find its errors**, not to confirm it. Assume every value may be wrong until you have checked it yourself. Accuracy matters more than speed. A cell you cannot verify must be reported as unverifiable, never guessed.

If you cannot browse the live web in this chat, say so now and stop. Do not audit from memory.

## 2. WHY THIS AUDIT MATTERS
I am a student at TISS writing a dissertation on whether India's AI data centre expansion is sustainable. For each data centre I will compare **district-level** electricity and water conditions to build a risk matrix. A wrong coordinate, a wrong district, an "operational" label on a site that is only announced, or an inflated MW figure would corrupt the whole analysis. The earlier versions of this dataset contained many such errors (section 9).

## 3. FRESHNESS
Use today's real date. Many facts changed in 2026. Search the web; do not rely on training memory.

## 4. WHAT YOU RECEIVE
A JSON array. Each object has these keys, in this order:

`id, record_type, parent_id, facility_name, operator, state, city, exact_location_address, latitude, longitude, coordinates_lat_long, google_maps_url, location_precision, operational_mw, true_development_status, workload_class, status_operational, power_procurement, cooling, investment, source, notes, district, planned_ultimate_mw, capacity_basis, year_operational_or_expected, as_of_date, verification_status`

What the builder was told (so you can check against it):
- `record_type`: `campus`, `phase` (inside a campus; `parent_id` set) or `programme` (multi-site, no coordinates, never added to totals).
- `location_precision`: `Exact site` (within about 100 m, confirmed on satellite imagery or an official document with coordinates), `Plot or village` (about 1 km), `Locality or industrial area` (about 5 km), `City centroid` (city only; not usable for site analysis), `District only` or `Unknown` (coordinates blank).
- `operational_mw`: MW **live and serving customers today** (never planned capacity, never a city or market total); `capacity_basis` says whether it is IT load or facility power.
- `true_development_status`: one of `Operational`, `Partially operational`, `Under construction`, `Approved, not started`, `Announced or MoU only`, `Planned or under evaluation`, `Stalled, cancelled or withdrawn`, `Unknown`. It must be judged by evidence of real activity, not announcements.
- `workload_class`: one to three values in brackets from `General, Colocation, Government, Hyperscale, AI-specific, AI-ready, Cloud, Enterprise Cloud, AI-native, Frontier AI, Unclassified, Mixed`. `AI-specific`, `AI-native` and `Frontier AI` need a source saying so.
- `source`: each URL tagged `[P]` primary (operator, filing, government order, state industrial body, environmental clearance, regulator), `[S]` reputable secondary (major news or trade press, market reports) or `[T]` tracker or lead only (Wikipedia, DataCenterMap, Baxtel, blogs), with an access date. Each key field needed one `[P]` source or two independent `[S]` sources. A `[T]` source alone is never enough.

## 5. INDEPENDENCE RULE
Do **not** assume the builder's sources are right. For each of **location, status and MW**, find **at least one source that is not already listed in the row's `source`**. If you can only find the same source, say so. Two articles that copy the same press release count as one source.

## 6. THE CHECKS

### A. Mechanical checks (whole file, before any web research)
Run these on the entire dataset first. If you can run code, do so. Otherwise check by hand and say which method you used.
- All keys are present, in the right order, with the right types. Numbers are plain numbers.
- Every `id` is unique. Every `parent_id` points to an existing `campus`.
- Every latitude and longitude lies inside India, and inside the stated state.
- `coordinates_lat_long` equals `latitude, longitude`. `google_maps_url` equals `https://www.google.com/maps?q=<latitude>,<longitude>`.
- Precision tier fits the data: tiers `District only` and `Unknown` have blank coordinates; `programme` rows have no coordinates.
- `operational_mw` is not greater than `planned_ultimate_mw`. Phase MW does not exceed the parent campus.
- `status_operational` is consistent with `true_development_status` and `operational_mw` (for example MW above 0 needs `Operational` or `Partially operational`; `Announced or MoU only` needs blank or 0).
- `workload_class` has only allowed values, in brackets, no more than three.
- No two campus rows share coordinates within 300 m (unless one is a phase of the other).
- No row relies only on `[T]` sources. `investment` states currency and scope. `source` follows the tag and date format.
- Report every failure by `id`.

### B. Source check (every URL in every row)
- Does the page open, and is it about this facility?
- Does the page actually support the claim attached to it? Give a short paraphrase of what it says and where (heading or section). Do not copy long passages.
- Is the tag right? (A news article tagged `[P]`, or a tracker tagged `[S]`, is an error.)
- Are two "independent" sources really the same press release or syndicated copy?
- Is the page dated, and does the date support "today"? A 2023 article cannot confirm a 2026 status.

### C. Location check (every row with coordinates)
- Find the site **by a method different from the builder's** (official address, environmental clearance documents, a government order naming the village or plot, or satellite imagery).
- Measure the distance between your point and the row's coordinates. Tolerances: `Exact site` 0.2 km, `Plot or village` 1 km, `Locality or industrial area` 5 km. Report the distance.
- Confirm the satellite view shows a data centre or construction (or the right empty plot for a planned site), not another company's building.
- Confirm `district` against the coordinates and the address, using **current** district names (for example Anakapalli was split from Visakhapatnam in 2022).
- Confirm `city` and `exact_location_address` match.

### D. Capacity and status check (every row)
- Is `operational_mw` truly live today? Look for a dated launch, commissioning or customer-service source. If only a plan exists, the value is wrong.
- Is it IT load or facility power, and does `capacity_basis` say the right one?
- Is it a single site, or has a city, market or company-wide total been entered as a facility? Has one commitment been split across rows?
- Does `true_development_status` match the evidence? Look specifically for construction proof (dated groundbreaking, tender award, satellite imagery) for `Under construction`.
- Look for **contradicting** news: delays, cancellation, ownership change, rename, acquisition, expansion.

### E. Other fields
- `operator`: correct company, including joint-venture partners and renamed or acquired companies.
- `workload_class`: does the evidence support each class? Flag any `AI-specific`, `AI-native` or `Frontier AI` without a source saying so.
- `power_procurement` and `cooling`: are they supported by a source? Company statements must be labelled "claimed". Flag unsupported statements.
- `investment`: correct amount, currency, scope (phase or whole project) and date.
- `year_operational_or_expected` and `as_of_date`: supported and current.

### F. Completeness check (after the row audit)
For each state, run an independent search for data centres that are **missing from the dataset** (operational, under construction or approved, at least 5 MW, or any AI-specific site). Use operator sites, state industrial bodies, approvals, environmental clearance documents, market reports and 2025–2026 news. List each missing candidate with a source and a note on whether it is a real site or a duplicate under another name.

### G. Duplicate and double-counting check
Look for the same site under different names, a campus and its phases both counted as separate campuses, and a company-wide figure split across rows.

## 7. VERDICT CODES
**Per field:**
- `OK`: you confirmed it with at least one source not in the row.
- `CORRECTED`: wrong, and you found the right value with a source.
- `UNVERIFIABLE`: you could not confirm it either way.
- `WRONG_NO_FIX`: it is wrong, and you could not find the right value (recommend leaving blank).

**Per row:**
- `PASS`: all key fields are `OK`.
- `PASS_WITH_FIXES`: some fields `CORRECTED`, the rest `OK` or `UNVERIFIABLE`.
- `FAIL`: location, status or MW is `WRONG_NO_FIX`, or the record is not a real facility.
- `DROP`: duplicate, market total, not a data centre, or out of scope (state why).

Never "fix" a value by guessing. Every correction needs a source.

## 8. PROCESS AND OUTPUT
1. Start by stating whether you can browse and run code.
2. Run check A on the whole file and report all failures.
3. Audit the rows in **batches of 10**. Wait for me to say "continue" before the next batch.
4. For each row, output one JSON object, one per line:

`{"id": "...", "row_verdict": "...", "location": {"result": "...", "distance_km": null, "corrected_latitude": null, "corrected_longitude": null, "corrected_district": null, "evidence": "..."}, "capacity": {"result": "...", "corrected_operational_mw": null, "evidence": "..."}, "status": {"result": "...", "corrected_status": null, "evidence": "..."}, "workload_class": {"result": "...", "corrected_value": null, "evidence": "..."}, "sources": {"result": "...", "problems": []}, "other_fields": {"result": "...", "corrections": {}}, "new_sources_found": [], "notes": "..."}`

Evidence strings contain the URL and a short paraphrase, never long quotations.

5. After the last batch, run check F (missing sites) and check G (duplicates).
6. Finish with a **final report**:
   - Counts of each row verdict.
   - Error rate by field (location, capacity, status, workload class, sources, other).
   - Location error distribution (how many within tolerance, how many outside, and the worst five distances).
   - Rows to drop, rows to correct, and the list of missing sites.
   - A go or no-go recommendation. My acceptance thresholds: at least 95% of coordinates within tolerance, at least 95% of statuses correct, no `[T]`-only rows, and no market totals counted as facilities. Say which thresholds are met and which are not.
7. Be concise. Do not ask me questions unless you are blocked. If something is uncertain, mark it and move on.

## 9. KNOWN ERRORS FROM EARLIER VERSIONS (look for these specifically)
- A "600 MW STT Hyderabad campus" was really CtrlS Chandanvelly's 40-acre, 600+ MW IT-load campus (text from a news roundup attributed to the wrong company).
- AIRAWAT is a supercomputer at C-DAC Pune, not a 600 MW data centre.
- A "Google Cloud Mumbai and Delhi NCR region" was wrongly filed in Visakhapatnam.
- AWS's 670 MW commitment was split into three rows (400 + 120 + 150) by a tracker.
- Wikipedia rows such as "Yotta Mumbai 289 MW" and "NTT Bengaluru 162 MW" were market totals, not single sites.
- Full build-out figures were shown as operational: NTT Kolkata 40 MW (about 6 MW IT load live), NTT Noida 2 at 52.8 MW (22.4 MW live), PDG MU1 at 150 MW (about 48 MW live).
- Reliance's Vizag cluster is in **Vizianagaram** district (Polipalli, Bhogapuram), not Visakhapatnam. Google's Vizag hub spans Visakhapatnam and Anakapalli districts.
- Some "locations" in trackers were only a city name, not a site.

## 10. THE DATASET TO AUDIT
(Paste the JSON array between the markers below, or upload it as a file.)

<DATASET>

</DATASET>
