# PROMPT: Build a verified dataset of data centres in India
(Paste everything below this line into a fresh chat with a model that has live web search.)

---

## 1. ROLE
You are a careful data researcher. Your job is to build a verified dataset of data centres in India. **Accuracy matters more than completeness.** A blank cell is always better than a wrong or guessed cell.

If you cannot browse the live web in this chat, say so now and stop. Do not fill the dataset from memory.

## 2. WHY THIS DATASET EXISTS
I am a student at TISS writing a dissertation on whether India's AI data centre expansion is sustainable. For each data centre location I will compare local electricity and water conditions at **district level** to build a risk matrix ("is it sustainable to place a data centre here?"). So these must be correct:
- where the site really is (coordinates and district),
- whether it really exists or is only an announcement,
- how many MW are actually live today.

My earlier versions were built from trackers and Wikipedia and contained many errors (see section 10). I am rebuilding from scratch and want every row checked.

## 3. FRESHNESS
Use today's real date. Many facts changed in 2026, so search the web for everything and do not trust your training memory. Record the date each fact was last checked.

## 4. SCOPE (editable defaults)
- **Geography:** all of India.
- **Include:** every data centre campus or facility that is operational, under construction, approved, or publicly announced with a named site, with at least **5 MW** (IT load or announced capacity). Also include any facility described as AI-specific or AI-ready, whatever its size.
- **Exclude:** small government State Data Centres under 5 MW; city or market totals (for example "Mumbai has 890 MW"); supercomputers that are not data centres; pure announcements with no company or no location named (put those under `programme`, see section 5).
- Work **state by state** until all states are covered. If you cannot cover a state, say so.

## 5. RECORD TYPES (variable `record_type`)
- `campus`: one physical site or campus with one location.
- `phase`: a building, phase or tenant facility inside a campus. Set `parent_id` to the campus `id`.
- `programme`: a multi-site commitment with no single location (for example "Company X will invest 5 GW across India"). No coordinates. It is kept for reference and **never added into totals**.

Rules to avoid double counting:
- Put capacity on the lowest level that has a figure. If a campus has phases, the campus row holds the campus total and the phases hold their parts. State in `notes` that they are nested.
- Never split one company-wide commitment across sites unless the company itself gave per-site numbers.

## 6. VARIABLES (22 required, in this order, then 6 recommended extras)

| # | JSON key | What it means and how to fill it |
|---|---|---|
| 1 | `id` | Unique code. `DC001`, `DC002`, ... Phases use the campus code plus a letter (`DC014a`). |
| 2 | `record_type` | `campus`, `phase` or `programme` (section 5). |
| 3 | `parent_id` | The campus `id` if this row is a `phase`. Blank otherwise. |
| 4 | `facility_name` | The official name used by the operator. If the operator has no name, use "Operator, locality". |
| 5 | `operator` | Company that owns or runs it. If different, write "Owner / Operator". For joint ventures list all partners. |
| 6 | `state` | Indian state or Union Territory. |
| 7 | `city` | City or town. Use the nearest town if it is rural, and put the village in variable 8. |
| 8 | `exact_location_address` | Full address, or plot and survey number, or village + mandal/taluka + district + state + PIN. Write only what a source states. Do not construct an address. |
| 9 | `latitude` | Decimal degrees, 6 decimals (for example `17.384712`). Blank if not verified. |
| 10 | `longitude` | Decimal degrees, 6 decimals. Blank if not verified. |
| 11 | `coordinates_lat_long` | Text in the form `17.384712, 78.456321`. Built from variables 9 and 10. Blank if they are blank. |
| 12 | `google_maps_url` | `https://www.google.com/maps?q=<latitude>,<longitude>`. Built only from verified coordinates. Blank otherwise. |
| 13 | `location_precision` | How exact the coordinates are. Use exactly one of the tiers in section 7. |
| 14 | `operational_mw` | Number only. MW that is **live and serving customers today**. Use `0` if confirmed none is live. Leave blank if unknown. **Never** put planned or full-campus capacity here, and never copy a city or market total. State the basis (IT load or total facility power) in `capacity_basis`. |
| 15 | `true_development_status` | The real stage, judged by evidence and not by press-release language. Use exactly one value from section 8. |
| 16 | `workload_class` | One to three values from this list only, written in normal text inside brackets, for example `[Hyperscale, AI-ready]`. See the definitions below. |
| 17 | `status_operational` | Simple flag. `Operational` (all or most of the stated capacity is live), `Partially operational` (phase 1 or some buildings live), or `Not operational`. |
| 18 | `power_procurement` | How the site gets its electricity: grid connection and voltage, utility (discom), named power purchase agreements, captive solar or wind (with MW), green open access, battery storage, stated renewable share. Write "Not disclosed" if no source states it. Label company claims as "claimed". |
| 19 | `cooling` | Cooling method and water source: air-cooled, evaporative, liquid or immersion, closed-loop; water from municipal supply, borewell, canal, desalinated seawater, treated sewage water; any stated water or PUE/WUE claim (labelled "claimed"). "Not disclosed" if unknown. |
| 20 | `investment` | Amount with currency and scope, for example `INR 70,000 crore (stated; whole campus; TCS release, 5 Sep 2026)`. Say whether it covers one phase or the whole project. Blank if not stated. Do not convert currencies unless asked. |
| 21 | `source` | Every URL used, each tagged by quality and access date. Format in section 9. |
| 22 | `notes` | Conflicts between sources, assumptions, what could not be verified, and nesting remarks. |

**`workload_class` allowed values and meaning**
- `General`: ordinary IT workloads.
- `Colocation`: rents space and power to several customers.
- `Government`: run for a government body.
- `Hyperscale`: very large campus built for or by big cloud or internet companies.
- `AI-specific`: operator states it is built for AI training or inference (GPU clusters). Needs a source saying so.
- `AI-ready`: designed for high-density AI racks (for example liquid cooling) but not only for AI.
- `Cloud`: hosts a public cloud region.
- `Enterprise Cloud`: private or enterprise cloud services.
- `AI-native`: designed from the ground up around AI infrastructure.
- `Frontier AI`: built for training or serving frontier models, with a named anchor customer (for example OpenAI or Meta). Needs a source.
- `Unclassified`: no reliable information. Use this instead of guessing.
- `Mixed`: clearly serves several of the above with no main one.

**Recommended extras (columns 23 to 28; I may delete them, but fill them)**

| # | JSON key | Meaning |
|---|---|---|
| 23 | `district` | District of the site. **Required for my risk matrix.** Use the current district name (for example Anakapalli was split from Visakhapatnam in 2022). |
| 24 | `planned_ultimate_mw` | Announced full build-out. Number only. Without this, planned sites would show no capacity at all. |
| 25 | `capacity_basis` | `IT load`, `Facility/grid load`, `Announced (unspecified)` or `Unknown`. |
| 26 | `year_operational_or_expected` | Year it went live, or the year the operator or government says it will. Add the word `target` if it is a target. |
| 27 | `as_of_date` | The date the capacity and status figures were last confirmed (YYYY-MM-DD). |
| 28 | `verification_status` | `Verified (primary)`, `Verified (2+ independent sources)`, `Partially verified` or `Unverified`. In `notes`, list which fields are not verified. |

## 7. LOCATION PRECISION (variable 13)
Use exactly one:
1. `Exact site`: coordinates sit on the actual building or plot and were confirmed on satellite imagery or by an official document that gives coordinates (about 100 m).
2. `Plot or village`: an official document names the village, plot or survey number, and coordinates are placed there (about 1 km).
3. `Locality or industrial area`: only the named industrial park or locality is known (about 5 km).
4. `City centroid`: only the city is known. Coordinates are the city centre. **Not usable for site-level analysis.**
5. `District only`: leave latitude, longitude, coordinates and URL blank.
6. `Unknown`: leave all location fields blank.

Coordinate rules:
- Never produce coordinates from memory. Every coordinate must come from a source that gives it, or from a place you actually located on a map or satellite view during this task.
- A coordinate is valid only if it passes all checks: it lies inside India; it lies inside the stated state; it is within the tolerance of the named village or locality; and a second independent source, or satellite imagery, agrees within about 1 km.
- If sources disagree by more than 1 km, do not guess. Put the higher-confidence one in the cells, lower the precision tier, and describe the conflict in `notes`.

## 8. TRUE DEVELOPMENT STATUS (variable 15)
Use exactly one value. Judge by evidence of real activity, not announcements.
- `Operational`: live and serving customers (customer launch, commissioning notice or an operator page showing service).
- `Partially operational`: some phase or building is live; the rest is not.
- `Under construction`: groundbreaking or construction is confirmed (dated news, a government event, tender award or satellite imagery).
- `Approved, not started`: state or central approval, or land allotted, but no construction evidence yet.
- `Announced or MoU only`: a statement or MoU with no approvals or land.
- `Planned or under evaluation`: the company says it is considering it.
- `Stalled, cancelled or withdrawn`: with the source.
- `Unknown`.

## 9. VERIFICATION RULES
**Source tiers (tag each source):**
- `[P]` Primary: operator website or press release, stock exchange filing, government order (GO), cabinet or SIPB minutes, state industrial development body allotment (APIIC, TGIIC, MIDC, GIDC, TIDCO and similar), environmental clearance documents (PARIVESH), regulator orders.
- `[S]` Reputable secondary: major news agencies and newspapers (PTI, Reuters, ET, Mint, The Hindu, Business Standard), trade press (DatacenterDynamics, Data Center Frontier), and city-level market reports from Cushman and Wakefield, JLL, CBRE or Colliers.
- `[T]` Tracker or lead only: Wikipedia, DataCenterMap, Baxtel, aggregator sites, blogs. **Use these only to find leads. Never rely on a `[T]` source alone.**

**What each key field needs:**
- Location, capacity, status and investment each need **one `[P]` source, or two independent `[S]` sources.** Otherwise leave the field blank (or mark the row `Unverified`).
- Two articles that copy the same press release are **one** source.
- If sources conflict, prefer the `[P]` one, and describe the other in `notes`.
- Never fill a cell by inference, by averaging, or because it "seems likely". Write "Not verified" in `notes` instead.
- Never turn a city or market total into a facility row.
- Capacity must say whether it is IT load or facility power. Do not mix them.

**`source` format:**
`[P] https://... (accessed 2026-10-23) ; [S] https://... (accessed 2026-10-23)`

## 10. KNOWN TRAPS FROM MY EARLIER VERSIONS (do not repeat)
- A "600 MW Hyderabad STT campus" was actually CtrlS Chandanvelly's 40-acre, 600+ MW IT-load campus. A line copied from a news roundup was attributed to the wrong company.
- AIRAWAT is a supercomputer at C-DAC Pune, not a 600 MW data centre.
- A "Google Cloud Mumbai and Delhi NCR region" was filed in Visakhapatnam.
- AWS's 670 MW commitment was split into three rows (400 + 120 + 150) by a tracker. Do not do this.
- Wikipedia rows for "Yotta Mumbai 289 MW", "NTT Bengaluru 162 MW" and similar were market totals, not single sites.
- Full build-out figures were shown as "operational": NTT Kolkata 40 MW (only about 6 MW IT load live), NTT Noida 2 at 52.8 MW (22.4 MW live), PDG MU1 at 150 MW (about 48 MW live).
- Reliance's Vizag cluster is in **Vizianagaram** district (Polipalli, Bhogapuram), not Visakhapatnam. Google's Vizag hub spans Visakhapatnam and Anakapalli districts.
- Some project locations in trackers were only a city name. Do not accept a city as an exact location.

## 11. PROCESS (follow in order)
1. **Discover.** For each state, search operator sites, state industrial bodies and IT departments, approvals (SIPB, cabinet), PARIVESH, stock exchange filings, market reports and news from 2024 to today. Use `[T]` sources to find candidates, not to confirm them.
2. **Verify location** for each candidate. Find an official or primary location, then confirm it on satellite imagery or a second independent source. Record the precision tier.
3. **Verify capacity and status.** Separate live MW from planned MW. Check for construction evidence.
4. **Remove duplicates and nest.** One physical site gets one campus row.
5. **Run the checks in section 12.**
6. **Output** in the format in section 13.

Starting leads (candidates to check, **not facts**): Navi Mumbai (Yotta NM1, NTT, CtrlS, STT, Sify Rabale, AdaniConneX, PDG MU1 and MU2, Digital Connexion Chandivali), Chennai (AdaniConneX, NTT, STT Chennai, PDG CH1, Yotta), Bengaluru (NTT), Hyderabad (Microsoft Chandanvelly, AWS, CtrlS Chandanvelly, TCS HyperVault, NTT-Neysa, STT, Oracle), Delhi NCR (NTT Noida, Yotta Greater Noida), Andhra Pradesh (Google Vizag, Reliance Polipalli, Sify, Digital Connexion, AM AI Factory, Anant Raj, Tillman, RMZ), Gujarat (Reliance Jamnagar, STT Dholera), West Bengal (NTT, Sify, STT, Tata Communications, Airtel Nxtra, Hiranandani Uttarpara), Rajasthan (STT Jaipur). Also find the ones I have missed: Pune, Kolkata, Odisha, Madhya Pradesh, Uttar Pradesh, Haryana, Punjab, Kerala and others.

## 12. QA CHECKS (run before you output; list any failures)
- Every latitude and longitude is inside India and inside the stated state.
- `google_maps_url` matches the coordinates exactly.
- No two campus rows share coordinates within 300 m (unless one is a phase of the other).
- Phase MW does not exceed the parent campus MW.
- `operational_mw` is never greater than `planned_ultimate_mw`.
- If `operational_mw` is above 0, the status is `Operational` or `Partially operational`. If the status is `Announced or MoU only`, `operational_mw` is blank or 0.
- `AI-specific`, `AI-native` and `Frontier AI` each have a source saying so.
- No row relies only on `[T]` sources.
- `investment` always states currency and scope.
- `programme` rows have no coordinates and no MW in totals.

## 13. OUTPUT FORMAT
- Output a **JSON array**, **one object per line**, using the exact JSON keys in section 6, in that order. Use `null` for blanks. Numbers must be plain numbers (no commas or units).
- Send rows in batches of **20 or fewer** per message. Wait for me to say "continue" before the next batch.
- After the last batch, give:
  1. A coverage table by state (number of rows, and how many at each precision tier).
  2. A list of **unresolved items** (what could not be verified and why).
  3. A list of **source conflicts**.
  4. A list of **candidates dropped**, with the reason.
- Be concise. Do not ask me questions unless you are blocked. If something is uncertain, mark it and move on.
