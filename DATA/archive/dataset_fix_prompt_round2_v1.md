# PROMPT: Round-2 fix of the data centre dataset (v2 to v3)
(Paste everything below this line into the agent that has access to my files `data_centres_india_v2.json`, `data_centres_india_v2.csv`, `changes_log_v2.csv`, `evidence_log_v2.json` and `dataset_fix_complete_report_v2.md`. The agent must be able to browse the live web and run code.)

---

## 1. ROLE AND RULES
You are fixing a dataset of data centres in India for the second time. An independent reviewer spot-checked v2 with live web search and found that **the evidence behind it is not checkable and several facts are wrong**. You are the **fixer, not the auditor**.

- **Do not certify your own work.** Do not write "GO", "verified", "0 errors", "0 warnings" or "100%". End with a self-check summary that says what changed and what is still unverified. An independent audit will follow in another chat.
- **A blank cell is better than a wrong cell.** If you cannot support a value with a source, blank it and mark the row `Partially verified` or `Unverified`. "Verified" must be earned, row by row.
- **Never invent.** No value from memory, inference, rounding, or because it "seems likely". Do not write rounded coordinates, round MW figures, or round dates to look precise.
- **Keep v1 and v2 untouched.** Write new `v3` files only.
- **No silent edits.** Every changed cell goes into the changes log with a deep-link source.
- If you cannot browse the live web, say so now and stop.
- Work in the **stages in section 9**. After each stage, stop, report briefly, and wait for me to say "continue".

## 2. WHY THIS DATASET EXISTS
I am a student at TISS writing a dissertation on whether India's AI data centre expansion is sustainable. For each data centre I will compare **district-level** electricity and water conditions to build a risk matrix. A wrong location, a wrong status (announced shown as live), or a wrong MW figure corrupts the whole analysis. Today's real date applies; many facts changed in 2026, so search the web and do not trust memory.

## 3. WHAT THE REVIEW FOUND IN V2

### 3.1 The evidence is not checkable (fix everything in this section first)
- 147 of 167 source URLs are bare homepages (for example `https://datacenterdynamics.com`, `https://www.ctrls.com`). 69 of 89 rows have no deep link at all. DC088 has no URL.
- 39 source entries come from PeeringDB, DataCenterMap or Baxtel but are tagged `[P]` or `[S]`. No source anywhere is tagged `[T]`.
- All 89 rows are labelled "Verified" (60 primary, 29 two sources). None is partial or unverified.
- In `evidence_log_v2.json`, the capacity "paraphrase" in all 89 rows just repeats the value ("Operational MW: 30; Planned ultimate MW: 150"). This is circular, not evidence.
- Many sources are vague phrases with no link ("ICRA Credit Rating Rationale", "TIA-942 Compliance Audit", "APIIC Land Allotment Orders", "SIPB Minutes", "Telangana ITE&C Dept").
- 46 of 49 entries in the changes log are tagged `[P]`, and most links are homepages.

**Required fix (applies to every row and every key field):**
1. Every source must be a **deep link to the exact page or document** (full URL with path), plus the **page's publication date** and your **access date**.
2. For each key field (location, district, operational MW, planned MW, status, workload class, investment, year), give at least one deep link and a **paraphrase of what the page says**, in your own words, that is **different from restating the field value**. For example: "Page says the first building delivered 22.4 MW of IT load in January 2024 and a second building is planned." No long quotations.
3. Source tiers are fixed by domain and type. You may not choose them:
   - `[P]` Primary: the operator's own site or press release, a stock exchange filing, a government order or portal (state, central, SEIAA/PARIVESH, APIIC, MIDC, TGIIC, IDCO and similar), a regulator order.
   - `[S]` Reputable secondary: major agencies and newspapers (PTI, Reuters, ET, Mint, The Hindu, Business Standard), trade press (DatacenterDynamics, Data Center Dynamics, W.Media), and market reports from Cushman and Wakefield, JLL, CBRE or Colliers.
   - `[T]` Lead only: Wikipedia, DataCenterMap, Baxtel, PeeringDB, datacenters.com, aggregators, blogs, press-release reprint sites. **These may never support a coordinate, MW, status or investment on their own.**
4. A row may be `Verified (primary)` only if its location, MW and status are each supported by a deep-linked `[P]` source. It may be `Verified (2+ independent sources)` only if each key field has two `[S]` sources that are not copies of the same release. Otherwise use `Partially verified` or `Unverified`. Expect many rows to drop to partial or unverified. That is correct and expected.
5. Rows or fields whose only support is a `[T]` source must be re-verified from `[P]` or `[S]` sources, or blanked.
6. Do not cite a source you did not open in this session.

### 3.2 Facts that were wrong or unsupported
Re-verify each, fix what is wrong, and record the source. These are leads, not proof; open the pages yourself.

| Row | Problem | Lead (verify yourself) |
|---|---|---|
| **DC042** Microsoft Chandanvelly | Marked "Under construction, 0 MW, year 2025 target". Microsoft's Hyderabad region became generally available on 6 Aug 2026 and was formally opened on 24 Sep 2026. | https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/ |
| **DC043, DC044** Microsoft Mekaguda, Shadnagar | Statuses depend on DC042's region status; check each site's own status from Microsoft or state sources. Do not assume. | |
| **DC077** Adani Naraj, Cuttack | Says clearance in "late 2024 / 2024". Reports date the Odisha High-Level Clearance Authority approval to **September 2026** (1 GW, about 250 acres at Naraj, ₹1.04 lakh crore). Cooling "river water heat exchange loop" and "OPTCL tie-ins" have no source. | https://india.entrepreneur.com/?p=100055 |
| **DC079** SentraForge, Puri | Existence, 120 MW and Puri district look right (approved Sept 2026, ₹22,634 crore). Replace the vague sources with deep links, and check whether the status is "Approved, not started" or under execution. | https://www.businesstoday.in/india/story/odisha-clears-sentraforge-ais-massive-rs22634-crore-sovereign-compute-project-558006-2026-09-26 |
| **DC085** RMZ-Colt, Vizag | Capacity (1.25 GW), 200 acres at Jagnadhapuram, Anandapuram mandal look right (approval around 1 Aug 2026). But the dataset says investment "USD 10 billion (~INR 83,000 crore), 2025". Reports say the data centre campus is about **₹1.77 lakh crore**, and the $10 bn is RMZ's wider Andhra Pradesh commitment (including a GCC park). | https://www.datacenterdynamics.com/en/news/colt-rmz-look-to-develop-gigawatt-scale-data-center-campus-in-vizag-india/ |
| **DC088** NTT NAV2 | Year "2024", investment "USD 1.5 bn (NTT releases)" and sources "ICRA / TIA-942" have no link. NAV2 was launched in **March 2025** (500 MW facility, 336 MW IT). NTT said three data centres were live, including a 50 MW one. 50 MW may be a minimum. | https://w.media/ntt-launches-500-mw-dc-campus-in-mumbai/ |
| **DC004** NTT NAV1 | 30 MW live (IT load) and 150 MW planned (facility load) are mixed under one basis. Separate or restate them with one basis each. | |
| **DC070** Reliance Jamnagar | Investment shows INR 10,00,000 crore, a company-wide capex figure, not this campus. The 3 GW master plan is marked "Under construction" with 3,000 MW planned. Only the 168 MW Meta facility has a primary source (Reliance release, 10 June 2026). Separate three things: the 168 MW Meta facility, the larger Phase 1 if a source exists, and the 3 GW master plan. Mark the master plan as announced unless a source shows construction. | https://www.ril.com/sites/default/files/2026-06/10062026_MR_Reliance_and_Meta_to_Develop_AI-Enabled_Data_Centre_in_Jamnagar_Gujarat.pdf |
| **DC055, DC056, DC082** Google hub | Parcels are given 600, 400 and 400 MW (1,400 MW). Sources describe a **1 GW** hub overall. The per-parcel figures have no source. | https://www.datacenterdynamics.com/en/news/google-confirms-15bn-data-center-project-in-andhra-pradesh-india/ |
| **DC057** AdaniConneX Vizag Tech Park | Check it is not the same project as the AdaniConneX part of the Google hub (the first awarded phase is 400 MW at Tarluvada). If it is a duplicate, merge it. | |
| **DC045, DC046** AWS | Status "Partially operational" with blank MW in the table, but "Operational" in the report text. Make the status consistent. Do not invent MW. Only record a per-site MW if a primary source gives it. | |
| **DC083** Sify Vizag | Investment ₹15,266 crore and "SIPB 2024". An earlier source gave ₹16,466 crore for the SIPB approval. Find the approval order or a report of it and resolve. | |
| **DC052** STT Meerkhanpet | "Up to 100 MW" and "MoU in Singapore Jan 2025" have no source. The only fact found elsewhere was a Rs 3,500 crore Telangana MoU with no MW. Source it or blank the MW. The `investment` cell is empty even though the note says Rs 3,500 crore. | |
| **DC041** CtrlS Chandanvelly | Check status. The company has announced 250 MW sanctioned for phase 1. Say what is live, if anything. | |

### 3.3 Missing projects
Search for and add if verified (otherwise list in `open_issues`):
- **CtrlS Rambilli** (Anakapalli district), reported at about 100 MW on about 49.93 acres.
- **TCS HyperVault, Anakapalli district**, reported at about 200 acres.
- Check whether any other Andhra Pradesh or Odisha approvals in 2026 are missing.
- Check whether Andhra Pradesh's planned total in the dataset (7,112 MW) double-counts overlapping projects or the Google hub.

### 3.4 Coordinates are rounded and some pins were moved to pass a check
- 30 rows have both coordinates rounded to 3 decimals or fewer (about 100 m or worse), 12 have 2 or fewer (about 1 km), and 31 have a coordinate ending in "000". "All 6 decimals verified" only means zeros were added.
- One `Exact site` (DC019, `18.590500, 73.738000`) has 3 decimals.
- DC030 (Colt Chennai) was moved about 0.6 km with no source naming its parcel. DC031 (CapitaLand Chennai) was moved and then upgraded to `Exact site`. DC009 was moved to a "corridor" pin. These moves cleared a proximity check without evidence.

**Required fix:**
- For each coordinate, record **how it was obtained** (official document with coordinates, address geocoding, or satellite imagery you looked at) and give the deep link.
- Re-assign `location_precision` to match the real accuracy: `Exact site` only for a coordinate supported to about 100 m; `Plot or village` for about 1 km; `Locality or industrial area` for about 5 km; otherwise `District only`.
- Where you cannot support a coordinate beyond locality, say so in the precision tier. Do not pad zeros to look precise. If a coordinate has fewer than 5 real decimals, the precision tier cannot be `Exact site`.
- A proximity flag is a reason to investigate, not a number to satisfy. Resolve each pair as a duplicate, a wrong pin, or a nested phase, with a source. Do not move a pin just to clear the flag.

### 3.5 Status, size and totals
- 10 rows are labelled `Operational` while only 18–69% of planned capacity is live (for example DC061 Yotta D1: 28.8 of 160 MW; DC063: 10 of 50; DC065: 16 of 50). By my rules these are `Partially operational` unless most of the stated capacity is live.
- DC040 (4.1 MW) and DC064 (4.5 MW) are under the 5 MW cutoff but still included, while other sub-5 MW sites were excluded citing that cutoff. Apply the cutoff consistently, or document an exception.
- The planned-capacity total (20,544.8 MW) mixes live, under-construction, approved, and MoU-only capacity. Report planned MW **split by status**, computed with code.
- Telangana shows only 21.8 MW operational, against about 151 MW (Cushman and Wakefield) and over 300 MW (Telangana government release, Sept 2026). Re-check Microsoft, AWS, CtrlS, and other live Hyderabad sites, and report which live capacity is still undisclosed.

### 3.6 Benchmark reconciliation looks fitted
- Kolkata is exactly 22.0 MW and Chennai 215.4 MW against benchmarks of 22 and 214, while other markets are explained away as "benchmark counts gross facility load". The explanation is applied selectively.
- "C&W estimates AWS at 100-120 MW" has no source.
- Remove explanations you cannot source. State each market's gap plainly and list the likely missing live sites you could not verify. Do not adjust any MW figure to hit a benchmark.

### 3.7 Self-certifying language
The v2 report says "0 Errors / 0 Warnings", "89 verified records" and "Integrity Status". Remove all of it.

## 4. VOCABULARY AND RULES (unchanged)
- `location_precision`: `Exact site`, `Plot or village`, `Locality or industrial area`, `City centroid`, `District only`, `Unknown`.
- `true_development_status`: `Operational`, `Partially operational`, `Under construction`, `Approved, not started`, `Announced or MoU only`, `Planned or under evaluation`, `Stalled, cancelled or withdrawn`, `Unknown`.
- `workload_class`: one to three of `General, Colocation, Government, Hyperscale, AI-specific, AI-ready, Cloud, Enterprise Cloud, AI-native, Frontier AI, Unclassified, Mixed`, in brackets. `AI-specific`, `AI-native` and `Frontier AI` need a source that says so.
- `verification_status`: `Verified (primary)`, `Verified (2+ independent sources)`, `Partially verified`, `Unverified`.
- `operational_mw` is MW **live today** with a dated source; never planned capacity. State the basis (`IT load` or `Facility/grid load`) and do not mix bases in one row.
- `investment` must state the figure, currency, **scope** (this campus, this phase, or a company-wide plan) and the date of the source. Do not use a company-wide figure as a campus investment.
- Cooling and power statements must be labelled "claimed" or "proposed" unless a primary source confirms them. Remove any statement with no source.
- Minimum size 5 MW (or AI-specific/AI-ready of any size).

## 5. HARD CHECKS (run with code before delivering, and show the results)
- Every URL in `source` and the evidence log has a path (not a bare domain), a publication date and an access date.
- No `[T]` domain (PeeringDB, DataCenterMap, Baxtel, datacenters.com, Wikipedia) is tagged `[P]` or `[S]`, and no key field relies only on a `[T]` source.
- No capacity "paraphrase" simply restates the field value.
- No `Exact site` coordinate has fewer than 5 real decimals. No coordinate is padded with trailing zeros.
- No two unrelated campuses within 300 m. Every pair under 500 m is explained with a source.
- Status and MW are consistent. `Operational` only if most of the stated capacity is live.
- All aggregates (state totals, shares, planned MW by status) are computed from the v3 file, not typed.
- Count of rows by `verification_status`. Do not force it to "all verified".

## 6. CHANGES LOG FORMAT
`changes_log_v3.csv`: `id, field, old_value, new_value, reason, evidence_url (deep link), page_date, access_date, source_tier`. Every change is listed, including blanking.

## 7. EVIDENCE LOG FORMAT
`evidence_log_v3.json`: for each row and key field: the deep link, page date, access date, source tier, and a **paraphrase of what the page says** (not the field value). Add a verdict: `OK`, `CORRECTED`, `UNVERIFIABLE` or `WRONG_NO_FIX`. Some rows should end up `UNVERIFIABLE`. That is honest.

## 8. OUTPUT FILES (new files; never overwrite v1 or v2)
- `data_centres_india_v3.json` and `data_centres_india_v3.csv` (same 28 keys, same order)
- `changes_log_v3.csv`
- `evidence_log_v3.json`
- `market_reconciliation_v3.csv`
- `open_issues_v3.md`
- `self_check_summary_v3.md`: what changed, counts by `verification_status`, error rates you found, and a plain statement that this is a self-check and **not an independent audit**.

## 9. STAGES (stop after each and wait for me to say "continue")
1. **Stage 1: Evidence audit of your own v2.** Show counts for section 5 (bare URLs, tracker sources tagged `[P]`/`[S]`, circular paraphrases, rounded coordinates). No file changes yet.
2. **Stage 2: Source repair.** Replace every vague or homepage source with a deep link, or mark the field unverified. Re-tag sources by the fixed rules. Re-assign `verification_status` honestly.
3. **Stage 3: The factual fixes in section 3.2 and 3.5.** Show before and after for every changed cell.
4. **Stage 4: Coordinates and precision (3.4).** Show the real accuracy and method for each coordinate.
5. **Stage 5: Missing projects (3.3) and market reconciliation (3.6).**
6. **Stage 6: Rebuild and report.** Run section 5 checks, write the outputs, write the self-check summary. No "verified", "0 errors" or "100%" wording.
