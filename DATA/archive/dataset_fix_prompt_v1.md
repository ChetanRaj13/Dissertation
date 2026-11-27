# PROMPT: Fix the data centre dataset (v1 to v2), based on a review of the audit report
(Paste everything below this line into the agent that has access to my files `data_centres_india_v1.json`, `data_centres_india_v1.csv` and `dataset_audit_report_v1.md`. The agent must be able to browse the live web and run code.)

---

## 1. ROLE AND RULES OF THIS PASS
You are fixing a dataset of data centres in India. An earlier "audit" of it was reviewed by an independent reader and found **not trustworthy**. In this pass you are the **fixer, not the auditor**. That means:

- **Do not certify your own work.** Do not write "GO", "100% verified" or "zero errors". At the end, write only a **self-check summary** saying what you changed and what is still unverified. A separate independent audit will follow in another chat.
- **Accuracy matters more than completeness and more than a clean result.** A blank cell is better than a wrong one. Rows that cannot be verified must stay marked `Unverified`, be blanked in the uncertain fields, or be dropped.
- **Never invent.** Do not fill a value from memory, inference, averaging or because it "seems likely". Every changed value needs a source.
- **Keep v1 untouched.** Write all outputs as new `v2` files. Never overwrite v1.
- **No silent edits.** Every changed cell goes into a changes log (section 9).
- If you cannot browse the live web, say so now and stop.
- Work in the **stages in section 8**. After each stage, stop, report briefly, and wait for me to say "continue".

## 2. CONTEXT
I am a student at TISS writing a dissertation on whether India's AI data centre expansion is sustainable. I will compare **district-level** electricity and water conditions for each data centre location to build a risk matrix. So location (coordinates, district), real status and real operational MW must be correct. Today's real date applies; many facts changed in 2026, so search the web and do not trust memory.

## 3. WHAT THE REVIEW FOUND (fix every item)

**3.1 The audit had no evidence.**
Rows showed "OK / OK" with no URLs. There were no FAIL, DROP or UNVERIFIABLE verdicts, and every threshold was exactly 100%. Not credible for 80 sites, many only announcements.
- Fix: build an evidence log (section 9) with, for every row and every key field (location, district, operational MW, status, workload class, investment), at least one URL and a short paraphrase of what the page says. Use honest verdicts, including `UNVERIFIABLE`, `WRONG_NO_FIX` and `DROP`.

**3.2 The auditor edited the data it was judging.**
Four coordinates were moved to clear a proximity check: `DC008`, `DC009`, `DC015` (moved 5.42 km) and `DC031`. Three of the new coordinates have only 3 decimals (about 100 m accuracy), yet other rows claim 0.02 km errors.
- Fix: restore the v1 coordinates for these four rows, then re-locate each site independently (official address, environmental clearance documents, a government or industrial-body land document, or satellite imagery). Use the new point only if a source supports it. All coordinates must have 6 decimals.
- Fix: **proximity rule.** Two campus rows within 300 m are allowed only if one is a phase or building of the other. "Adjacent industrial plots" is not an exception. Resolve each pair as a duplicate, a wrong pin or a genuine same-campus nesting.
- Check specifically: `DC009` (Digital Connexion BOM10) and `DC013` (Equinix) both reference the "Boomerang parcel" in Chandivali. Are they really different sites?

**3.3 The location precision tiers were not the ones I defined.**
The report used a made-up "Rooftop centroid" tier. Allowed tiers are only: `Exact site` (within about 100 m, confirmed on satellite imagery or an official document with coordinates), `Plot or village` (about 1 km), `Locality or industrial area` (about 5 km), `City centroid`, `District only` and `Unknown`.
- Fix: relabel every row to an allowed tier based on the evidence. Downgrade any row whose coordinates you cannot confirm to the tier you can support.

**3.4 PeeringDB was used as proof of location.**
PeeringDB is a network registry with self-reported pins. It is a lead, not proof. For example `DC004` was "verified" against a PeeringDB pin.
- Fix: any coordinate whose only support is PeeringDB, DataCenterMap, Baxtel, Wikipedia or a similar tracker must be re-verified from a primary source or satellite imagery, or its precision tier must be lowered and `verification_status` set to `Unverified`.

**3.5 Impossible arithmetic.**
The report said Mumbai plus Chennai hold 848.1 MW (72.5%) of 1,170.6 MW. But the report's own table gives Maharashtra 592.7 + Tamil Nadu 215.4 = 808.1 MW, and Maharashtra also includes Pune. The maximum possible share is 69.0%.
- Fix: delete that claim. Recompute every aggregate **with code from the v2 file** (state, district and metro totals, shares). Do not type totals by hand. Put the recomputed table in your output.

**3.6 The completeness claim is contradicted by market benchmarks.**
The report said no operational site of 5 MW or more was missed. Yet the dataset totals 1,170.6 MW operational, against about 1,789 MW in Cushman & Wakefield's H1 2026 top-7 markets. Benchmarks (operational MW): Mumbai 890, Chennai 214, Delhi NCR 183, Bengaluru 162, Hyderabad 151, Pune 133, Kolkata 22. The dataset's state totals are Maharashtra 592.7 (including Pune), Karnataka 91.5, Uttar Pradesh plus Haryana 118.0 and Telangana 121.8.
- Fix: for each market, list the operational sites in the dataset and reconcile to the benchmark. For every gap above about 20 MW, search for the missing operational sites (operator sites, state industrial bodies, environmental clearance documents, news from 2024 to today). Add each verified site as a new row. If a gap remains, state it, and note possible reasons (benchmark counts capacity differently, IT vs facility load, site below 5 MW).
- Fix: run a **missing-site sweep for every state**, not only the big ones. List candidates found, with sources, including those you rejected and why.

**3.7 Google's Vizag hub is incomplete.**
The report listed two parcels (Tarluvada 266.6 acres and Rambilli 174.8 acres, total 441.4 acres). The state's total is 601.4 acres. My earlier research found a third parcel, **Adavivaram-Mudasarlova (about 160 acres)** in Visakhapatnam district.
- Fix: verify and add the third parcel with its own row (or nested phase rows) and its source. Confirm the total acreage against the Andhra Pradesh order or a primary or major news source.

**3.8 Missing Andhra Pradesh projects.**
The dataset has only a small Sify "AI Edge" site at Rushikonda in Visakhapatnam (`DC058`), which is not the 500 MW Sify project.
- Fix: check and add, if verified, each of these with approvals, site, capacity and status: Sify's 500 MW Vizag campus, Digital Connexion's 1 GW Vizag campus (MoU), Anant Raj (about 300 MW), RMZ (MoU), and any others found. For each, record the village or mandal if a source gives it. Otherwise leave coordinates blank and use `District only`.

**3.9 The AWS commitment was split into sites (a known trap).**
`DC045` and `DC046` show "50 MW live" each, derived from a 670 MW commitment. AWS does not publish per-site MW.
- Fix: make AWS's India commitment a `programme` row (no MW in totals). Keep an AWS campus row only if a primary source names that campus; leave `operational_mw` blank unless a primary source gives it. Record the site location only to the precision a source supports.

**3.10 STT Meerkhanpet "100 MW" has no source I can find.**
The only STT Hyderabad fact I found was an MoU of about Rs 3,500 crore with no MW.
- Fix: find a primary source for `DC052`'s existence, location and MW. If none exists, blank the MW, set `Announced or MoU only` (or `Unverified`), and set precision to what the source supports.

**3.11 Reliance Jamnagar was mislabelled.**
`DC070` says "168 MW Phase 1 Meta anchor". The 168 MW is the **Meta facility** (Reliance release, 10 June 2026, delivery within two years). Reliance's Phase 1 and the 3 GW master plan are separate, larger figures.
- Fix: separate the rows or fields so the 168 MW Meta facility, the larger Phase 1 and the master plan are not mixed. Nest them with `parent_id`. Count each megawatt once.

**3.12 Cooling and power claims were overstated.**
The report said AP facilities (`DC054`, `DC055`, `DC057`) and `DC070` are "integrating captive seawater desalination". I found: Reliance Jamnagar says desalinated seawater cooling (company release); Google Vizag has seawater cooling only "proposed"; Reliance Vizag has a state water tariff subsidy but no confirmed source of water.
- Fix: for each row, write only what a source states, labelled "claimed" or "proposed" where appropriate. Otherwise "Not disclosed".

**3.13 Wrong or unsourced statements in the report.**
- "Newly bifurcated districts (Raigad, Chengalpattu, Anakapalli, Vizianagaram, Hooghly)" is wrong. Raigad and Hooghly were not newly split. Chengalpattu (2019) and Anakapalli (2022) were. Correct this.
- "Telangana DISCOMs have RPO compliance below 60%", "Chennai and Chengalpattu groundwater is Critical or Over-Exploited", and the installed renewable capacity figures for Gujarat (53,635 MW) and Rajasthan (50,718 MW) have **no sources**. The old RPO rules have also been replaced by the Renewable Consumption Obligation (RCO).
- The paragraph saying the data "proves the core policy thesis" is an inference, not an audit finding.
- Fix: remove these statements from the audit report, or keep them only with a dated primary source (CGWB for groundwater, MNRE or CEA for renewable capacity, regulator orders for RPO or RCO). Remove analysis and conclusions from the audit report altogether; they do not belong there.

**3.14 Operational MW needs a clear basis.**
- Fix: for every row with `operational_mw` above 0, record a dated source for what is live today and set `capacity_basis` (`IT load` or `Facility/grid load`). Known corrections from my research (re-verify yourself): NTT Noida 2 has 22.4 MW live of 52.8 MW; PDG MU1 has about 48 MW live of 150 MW; NTT Kolkata's first building is about 6 MW IT load of 40 MW. Never put planned or full-campus capacity in `operational_mw`.

## 4. FACTS I ALREADY FOUND (use as cross-checks; re-verify, do not just copy)
- Microsoft's Hyderabad region became generally available on 6 Aug 2026 and was formally opened on 24 Sep 2026 (Chandanvelly, Rangareddy). No MW figure found.
- Reliance's Vizag AI data centre is in **Vizianagaram** district: 854.97 acres allotted across Polipalli, Bhogapuram West and Bhogapuram East villages (Andhra Pradesh order Ms No. 30, 20 May 2026).
- Google's Vizag hub: Tarluvada (266.6 acres), Adavivaram-Mudasarlova (160 acres), Rambilli in Anakapalli district (174.8 acres), total 601.4 acres.
- CtrlS Chandanvelly: 40 acres, over 600 MW IT load when fully developed; this is the campus mistakenly attributed to STT in some roundups.
- AM AI Factory (512 MW) was approved on 22 Aug 2026 at Amanam village, Visakhapatnam district.
- Reliance-Meta Jamnagar: 168 MW facility, release dated 10 Jun 2026.

## 5. SOURCE RULES (apply to every changed or kept value)
- `[P]` Primary: operator website or press release, stock exchange filing, government order, cabinet or investment-board minutes, state industrial body allotment, environmental clearance documents (PARIVESH or state authority), regulator order.
- `[S]` Reputable secondary: major agencies and newspapers, trade press (DatacenterDynamics and similar), city market reports from Cushman and Wakefield, JLL, CBRE or Colliers.
- `[T]` Lead only: Wikipedia, DataCenterMap, Baxtel, PeeringDB, aggregators, blogs. **Never the only support for a value.**
- Location, operational MW, status and investment each need one `[P]` source or two **independent** `[S]` sources. Two articles copying one press release count as one source.
- If sources conflict, prefer `[P]`, and describe the other in `notes`.

## 6. VOCABULARY (unchanged)
- `location_precision`: `Exact site`, `Plot or village`, `Locality or industrial area`, `City centroid`, `District only`, `Unknown`.
- `true_development_status`: `Operational`, `Partially operational`, `Under construction`, `Approved, not started`, `Announced or MoU only`, `Planned or under evaluation`, `Stalled, cancelled or withdrawn`, `Unknown`.
- `workload_class`: one to three of `General, Colocation, Government, Hyperscale, AI-specific, AI-ready, Cloud, Enterprise Cloud, AI-native, Frontier AI, Unclassified, Mixed`, in brackets. `AI-specific`, `AI-native` and `Frontier AI` need a source that says so. In the earlier fix, 14 rows were relabelled to `Enterprise Cloud`, `Colocation` or `Cloud`: re-check that each relabel is supported by a source, not just a vocabulary match.
- `verification_status`: `Verified (primary)`, `Verified (2+ independent sources)`, `Partially verified`, `Unverified`.

## 7. HARD CHECKS (run with code before delivering)
- All coordinates have 6 decimals, lie inside India and inside the stated state, and `coordinates_lat_long` and `google_maps_url` match them exactly.
- Blank coordinates for `District only`, `Unknown` and `programme` rows.
- No two campus rows within 300 m unless one is a nested phase of the other.
- `operational_mw` is not greater than `planned_ultimate_mw`; phase MW does not exceed the parent campus.
- `operational_mw` above 0 requires `Operational` or `Partially operational`; `Announced or MoU only` requires blank or 0.
- No row relies only on `[T]` sources. `investment` states currency and scope.
- Every total you report is computed from the file, not typed.

## 8. STAGES (stop after each and wait for me to say "continue")
1. **Stage 1: Plan and mechanical review.** Confirm you can browse and run code. List all issues in section 3 that apply to specific row IDs (for example `DC004`, `DC008`, `DC009`, `DC013`, `DC015`, `DC031`, `DC045`, `DC046`, `DC052`, `DC058`, `DC070`). Do not change files yet.
2. **Stage 2: Location fixes.** Items 3.2, 3.3 and 3.4. Re-locate rows, fix tiers and coordinates, resolve proximity pairs. Show before and after for every row changed.
3. **Stage 3: Capacity, status and cooling fixes.** Items 3.9 to 3.12 and 3.14.
4. **Stage 4: Missing sites.** Items 3.6, 3.7 and 3.8, plus the all-state sweep. Show the market reconciliation table (benchmark vs dataset) before adding rows.
5. **Stage 5: Rebuild and report.** Recompute all aggregates (3.5), apply section 7 checks, write all output files, and write the self-check summary.

## 9. OUTPUTS (new files, same folder; never overwrite v1)
- `data_centres_india_v2.json` and `data_centres_india_v2.csv` (same 28 keys, same order).
- `changes_log_v2.csv`: columns `id, field, old_value, new_value, reason, evidence_url, source_tier, date_checked`. Every changed cell is listed. Silent changes are not allowed.
- `evidence_log_v2.json`: for each row and each key field, the URLs and a short paraphrase of what each page says (no long quotations), plus your verdict (`OK`, `CORRECTED`, `UNVERIFIABLE`, `WRONG_NO_FIX`).
- `market_reconciliation_v2.csv`: benchmark vs dataset for each market, with the gap and explanation.
- `open_issues_v2.md`: everything still unverified, disputed or dropped, and why.
- `self_check_summary_v2.md`: what changed, counts by verdict, honest error rates by field, and a plain statement that this was a self-check and **not an independent audit**.
