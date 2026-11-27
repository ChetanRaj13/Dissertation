##### **Context from m2023bsasass013@stud.tiss.edu | DISSERTATION 3**



**TASK:**

**Chetan (TISS, B.S. Analytics \& Sustainability Studies) is writing a dissertation assessing whether India's AI data centre expansion is sustainable, by comparing each data centre's water/power demand against the real capacity and stress level of its district. This chat covered: building a master dataset and Google Sheet, verifying 90+ data centre coordinates through real research, designing water/energy risk-scoring formulas, and producing handoff materials (agent.md, JSON data files, a comprehensive methodology write-up) for an external AI agent to build an India-wide map + KPI dashboard.**



**CURRENT STATE:**

**- Master Google Sheet built (12 tabs: data centres, groundwater, tap water, power, grid/DISCOM ratings, coordinates, README) from 11 source files Chetan provided.**

**- Coordinate research: started at 22 of 118 sites located, ended at 90 of 118 (76%) — each individually verified against operator name/facility code/review text, not blind geocoding. 26 sites confirmed (two independent research rounds) to have no public location data at all; 2 earlier "DO NOT USE" unverified candidates excluded. Primary sources used: PeeringDB (operator's own listings), government Environmental Clearance/Gazette/SEZ filings, decoded Google Plus Codes, Google Places cross-checked against operator/review text.**

**- Water-risk and energy-risk scoring formulas fully designed (CGWB 4-band groundwater categories, DISCOM-health-weighted energy risk, multiplicative demand-amplification combination, equal-weighted overall score) — grounded in real peer-reviewed/industry literature (WRI Aqueduct, LBNL/Green Grid WUE benchmarks, AHP weighting precedent). Designed but not yet computed against full data.**

**- A "Water Equity" dimension (JJM tap-coverage-based) was designed as a separate, non-blended metric — found zero districts are both groundwater-over-exploited AND tap-coverage-underserved at the tested threshold; Bengaluru Urban is the closest real example (177% over-exploited, 72.6% tap coverage).**

**- Dashboard project (separate task, now handed off to Chetan's own AI agent): agent.md written and twice revised — now specifies a plain HTML/CSS/JS (no framework) two-view dashboard (India groundwater map + KPI/charts summary page), reads a forthcoming design.md for styling. Three clean JSON files produced: data\_centres.json (118 sites joined with coordinates), groundwater\_districts.json (29 districts with CGWB categories), summary\_stats.json (10 KPIs + 7 chart datasets, computed correctly with IT-load and facility-load kept separate after an initial mixing error was caught and fixed).**

**- A comprehensive "Data Collection Methodology" Google Doc was built across two chats: original 8 sections (purpose, scope, per-dataset methodology, source tiers, limitations) plus 3 new sections added in this chat — Section 9 (consolidated source inventory by \[P]/\[S]/\[T] tier), Section 10 (verification/cross-checking methodology with real rejected-match examples), Section 11 (data quality assurance measures). Doc link: https://claude.ai/artifact/NqTGBvQG7jnGHM2nJijkAp**



**KEY CONTEXT:**

**- Headline numbers: 114 data centre campuses (+4 phase sub-rows), 14 states, 29 hosting districts. Live capacity 1,380.5 MW IT load / 37.0 MW facility load. Planned capacity 9,362.9 MW IT load / 9,141.0 MW facility load (planned ≈6.8x live). Verification confidence: 25 backed by 2+ sources, 40 by one primary source, 48 partial, 1 unverified.**

**- Groundwater: 8 of 29 districts already over-exploited (Gurugram worst at 194.6%), using CGWB's official 4-band system (Safe <70%, Semi-critical 70–90%, Critical 90–100%, Over-exploited >100%) — deliberately chosen over WRI Aqueduct's global bands as the India-appropriate regulatory standard.**

**- Chetan's preferences: works one step at a time with explicit confirmation on big actions; wants plain-language reasoning behind every decision; cost-conscious; explicitly rejected blind/automated shortcuts in favor of verified accuracy (chose real web research over fast geocoding once the failure rate became clear); wants copyable/exportable outputs; non-technical but comfortable with numbers when explained simply.**

**- Two files still outstanding from Chetan before the dashboard can be built: India district boundary GeoJSON, and the CGWB National Compilation of Ground Water Resources (nationwide PDF) — offered to extract the PDF directly if uploaded, to keep schema consistent with the 29-district version already built.**

**- Real example used throughout: CORE13 (Microsoft's Ranga Reddy facility) explicitly uses "zero-water, air-cooled chillers" — illustrates the water-energy tradeoff discussed (air cooling shifts water burden to India's coal-heavy electricity grid rather than eliminating it).**



**ETHICAL CONSIDERATIONS SURFACED:**

**- No human subjects or personal data involved anywhere in this research — it is entirely desk-based secondary analysis of public government records, corporate disclosures, and infrastructure data. Worth stating explicitly in the ethics assignment as a low-risk-to-individuals research design.**

**- Heavy reliance on government and regulatory data (CGWB, JJM, CEA, PFC Integrated Rating, MoEFCC/SEIAA Environmental Clearance filings, SEZ/Gazette notifications) raises a data-provenance and currency question: some figures (e.g. DISCOM ratings) were only accessible via third-party mirrors (a JMK Research PDF, a Scribd upload) rather than the regulator's own site — flagged honestly in the methodology as a limitation, not hidden.**

**- The research topic itself surfaces a real social-equity tension worth discussing substantively: data centres competing for groundwater and electricity in districts where local communities' basic access (tap water coverage, reliable power) is not yet universal — the "Water Equity" analysis (Section on JJM/CGWB compounding) was built specifically to surface this, finding Bengaluru Urban as the sharpest real example of resource stress coexisting with incomplete community water access.**

**- Source material surfaced genuine land-use conflicts connected to specific data centre projects: a PIL (Public Interest Litigation) was filed alleging illegal allocation of land (including land with religious/temple significance) for the Google/Adani Visakhapatnam data centre project, and separate reporting raised concerns about Dalit farmers' land being acquired for the same project. These are facts about the research subject matter found in secondary sources (Land Conflict Watch, Deccan Chronicle, New Indian Express), not actions taken by Chetan's own research — but they are directly relevant ethical context for a dissertation on data centre sustainability, since they point to a social-justice dimension beyond pure resource metrics.**

**- Heavy use of AI-assisted web-search tools as a research methodology raises a reliability/integrity question, which was explicitly addressed as a safeguard: AI tool outputs and self-reported "verified" claims were never accepted at face value; every claim was independently cross-checked against operator names, official filings, or review text, and specific false-positive matches were caught and rejected (documented with real examples in Methodology Doc Section 10). This is itself a responsible-research-practice safeguard worth describing in the ethics assignment, not just a technical detail.**

**- Transparency about uncertainty was treated as a first-class design requirement throughout — every coordinate carries an explicit precision tier, every data centre entry carries a verification-confidence tag, and 26 sites are honestly marked as unlocatable rather than estimated. This reflects a deliberate commitment to not overclaiming certainty in reported data, directly relevant to "ethical reasoning and justification" and "proposed safeguards" in the assignment rubric.**

**- No commercial or personal conflict of interest is present — all source data is already public, and Chetan has no commercial relationship with any company whose data centres appear in the dataset.**



**WHAT TO IGNORE:**

**- The abandoned attempt to build the Google Sheet by relaying raw base64 content through tool calls (superseded by a working xlsx-upload approach).**

**- Superseded/old dataset files (v1/v2 versions, duplicate grid files, rejected coordinate candidates CORE35/CORE77/CORE72-old/CORE71-old).**

**- Any "100% verified"/"0 errors" self-claims from AI search tools — explicitly never trusted, not a real finding.**

**- Repeated or duplicate verification rounds already exhausted (a 6th coordinate search round on the 26 unlocatable sites was explicitly recommended against — confirmed unresolvable with current public information).**

**- News-based power figures and early research-framing options superseded by later, more authoritative sources.**



## **Context from m2023bsasass013@stud.tiss.edu | DISSERTATION 2**



**\*\*TASK\*\***



**Chetan (TISS, B.S. Analytics and Sustainability Studies) is writing a dissertation on whether India's AI data centre expansion is sustainable. This chat built a verified list of data centre sites in India, with state and district, true status, live and planned MW, and power and cooling facts. It also prepared district-level electricity and water indicators for a location risk matrix. The scoring is not part of this chat's task; only sourced inputs are.**



**\*\*Immediate next step (awaiting Chetan):\*\* upload the CGWB 2025 district-wise groundwater annexure (https://cgwb.gov.in/en/ground-water-resource-assessment-0), which Claude could not access. Claude then extracts, for the 29 districts below, the annual extractable resource, extraction by use, stage of extraction, category and net availability for future use.**

**- \*\*Andhra Pradesh:\*\* Anakapalli, Guntur, Visakhapatnam, Vizianagaram**

**- \*\*Bihar and Chhattisgarh:\*\* Patna, Raipur**

**- \*\*Delhi:\*\* South East Delhi**

**- \*\*Gujarat:\*\* Ahmedabad, Gandhinagar, Jamnagar**

**- \*\*Haryana:\*\* Gurugram, Panchkula, Sonipat**

**- \*\*Karnataka:\*\* Bengaluru Rural, Bengaluru Urban**

**- \*\*Madhya Pradesh:\*\* Indore**

**- \*\*Maharashtra:\*\* Mumbai Suburban, Pune, Raigad, Thane**

**- \*\*Odisha:\*\* Khordha, Puri**

**- \*\*Tamil Nadu:\*\* Chengalpattu, Chennai, Kanchipuram**

**- \*\*Telangana:\*\* Ranga Reddy**

**- \*\*Uttar Pradesh:\*\* Gautam Buddha Nagar**

**- \*\*West Bengal:\*\* Hooghly, North 24 Parganas**



**Later items are Jal Jeevan Mission district tap coverage (ejalshakti.gov.in/jjmreport/JJMIndia.aspx), district hours of power supply (npp.gov.in) and map coordinates.**



**\*\*CURRENT STATE\*\***



**\*Final dataset (declared done enough; Chetan wants to stop the verification loop)\***

**- \*\*Files:\*\* `data\\\\\\\_centres\\\\\\\_final\\\\\\\_v1\\\\\\\_2.json` and `.csv`, plus `fixes\\\\\\\_applied\\\\\\\_v1\\\\\\\_2.csv`, in `/mnt/user-data/outputs/`. v1\_2 is the agent's v1\_1 with my one downgrade (CORE124) and a typo fix.**

**- \*\*Contents:\*\* 118 rows (114 campuses and 4 nested phases: CORE01a/b/c in Google's Vizag hub and CORE02a in Reliance Vizianagaram), in 14 states. 29 district groups plus 2 rows with no district (CORE16 NTT-Neysa, CORE119).**

**- \*\*MW by basis (never mix the bases):\*\***

&#x20; **- Live: 1,380.54 MW IT load and 37.0 MW facility load.**

&#x20; **- Planned: 9,362.9 MW IT load and 9,141.0 MW facility load, 18,503.9 MW in total.**

&#x20; **- The agent's summary wrongly says 9,332.90 and 31 groups.**

**- \*\*Verification:\*\* 49 partially verified, 40 primary, 28 with 2+ independent sources, 1 unverified.**

**- \*\*Coordinates:\*\* all blank. The agent had no geocoder or satellite view. Every row has a Google Maps search link for manual pinning.**

**- \*\*Schema (33 fields):\*\* `id, record\\\\\\\_type, parent\\\\\\\_id, facility\\\\\\\_name, operator, state, district, location\\\\\\\_detail, location\\\\\\\_precision, maps\\\\\\\_search\\\\\\\_url, latitude, longitude, operational\\\\\\\_mw, planned\\\\\\\_ultimate\\\\\\\_mw, capacity\\\\\\\_basis, true\\\\\\\_development\\\\\\\_status, status\\\\\\\_operational, workload\\\\\\\_class, power\\\\\\\_procurement, cooling, investment, key\\\\\\\_dates, verification\\\\\\\_status, sources, gaps\\\\\\\_or\\\\\\\_conflicts, district\\\\\\\_source\\\\\\\_url, coordinate\\\\\\\_method, coordinate\\\\\\\_source\\\\\\\_url, coordinates\\\\\\\_lat\\\\\\\_long, google\\\\\\\_maps\\\\\\\_url, location\\\\\\\_checked\\\\\\\_date, operational\\\\\\\_mw\\\\\\\_as\\\\\\\_of, evidence\\\\\\\_ref`.**

**- \*\*Chetan's agent files (on his machine):\*\* evidence log, URL registry (251 distinct URLs cited), change log, gap tables, `district\\\\\\\_indicators\\\\\\\_v1\\\\\\\_1.json` (31 rows with state-level energy and groundwater only; all district water, Jal Jeevan Mission and hours-of-supply fields null), 22 excluded sub-5 MW sites, and a dropped-candidates file.**

**- \*\*My earlier files (in outputs):\*\* `verified\\\\\\\_core\\\\\\\_v1.json` (30 rows from sources I read myself), the old `facilities\\\\\\\_merged\\\\\\\_v2.json` (low trust), `city\\\\\\\_benchmarks\\\\\\\_v1.json`, `dc\\\\\\\_location\\\\\\\_risk\\\\\\\_inputs\\\\\\\_v1.tsv`, and the prompt files (rebuild, audit, fix, round-2, next-pass, master prompt and context brief).**



**\*Process history\***

**- \*\*Earlier rounds:\*\* several agents built and "fixed" the dataset, and each round was reviewed by me.**

&#x20; **- \*\*Problems found:\*\***

&#x20;   **- Invented URLs and dates.**

&#x20;   **- Homepages cited as evidence.**

&#x20;   **- Trackers (PeeringDB, DataCenterMap, Baxtel, Wikipedia) tagged primary.**

&#x20;   **- Totals fitted to consultant benchmarks.**

&#x20;   **- An auditor editing the data it audited.**

&#x20;   **- AWS and Google MW split into invented per-site figures.**

&#x20;   **- Self-certification ("0 errors").**

&#x20;   **- Boilerplate engineering detail presented as fact.**

&#x20;   **- Reports that disagreed with their own JSON.**

&#x20; **- \*\*Remedy:\*\* I wrote the staged prompts.**

**- \*\*Final work:\*\* done by Gemini with search snippets and Python only. Its URLs came from its own searches, but 113 of 289 queries contained the URL path, so I suggested Chetan open about 15 links himself. He has not yet.**

**- \*\*My code check of the last fix round:\*\* no compound districts, sub-5 MW sites moved out, CORE80 relabelled "Partially operational", 0 bare homepages, 0 URLs missing from the registry, indicators consistent with the data.**

**- \*\*My corrections:\*\***

&#x20; **- STT Hyderabad's 100 MW is supported by STT's own release (Meerkhanpet, Mucherla, Ranga Reddy; MoU 18 Jan 2025; ₹3,500 crore). My earlier "MW not found" was wrong.**

&#x20; **- CORE124 (L\&T Panvel) was downgraded to "Partially verified": only a 2 MW pilot is confirmed and the 42 MW planned figure has no source.**

&#x20; **- CORE106 (L\&T Mahape, 40 MW under construction, groundbreaking 21 Jan 2026) is fine.**

**- \*\*Accepted remaining weaknesses:\*\***

&#x20; **- Evidence paraphrases are still templated.**

&#x20; **- Operator capacity pages count as "primary" but are not independent.**

&#x20; **- NTT NAV2 shows 50 MW live, against ICRA's 43 MW (Aug 2025).**

&#x20; **- L\&T Kanchipuram shows 30 MW live, against a weak source saying 12 MW.**

&#x20; **- The Kolkata "22.4 MW before CtrlS" note looks like fitting to the benchmark.**

&#x20; **- CtrlS rows total 162.4 MW against ICRA's 150 MW (Oct 2026) and the CEO's 370 MW claim.**

&#x20; **- AdaniConneX named cities sum to 60.6 MW against company totals of 51.0, 55.8 and 65.4 MW, so a 4.8 MW block is not itemised.**



**\*\*KEY CONTEXT\*\***



**\*Preferences\***

**- One step at a time with explicit confirmation before proceeding.**

**- Plain language, short answers, and the reason a fix works.**

**- Copyable output (JSON, TSV or markdown for Excel).**

**- Distinct download names for files with the same name, plus the exact destination path.**

**- Cost-conscious, not technical, and tired of the verification loop.**

**- Tags in his sheet: \*\*\[S]\*\* for data or research, \*\*\[I]\*\* for my inference.**



**\*Data rules agreed\***

**- \*\*Source tiers:\*\* \[P] operator pages or releases, filings, government orders, regulators. \[S] major news, trade press, rating reports, consultants. \[T] trackers and Wikipedia, never the sole support.**

**- \*\*URLs and dates:\*\* URLs only if a tool returned them. Homepages are not evidence. Page dates only if visible.**

**- \*\*Precision tiers:\*\* `Exact site` (about 100 m, needs a stated coordinate or satellite view), `Plot or village` (about 1 km), `Locality or industrial area` (about 5 km), `City centroid`, `District only`, `Unknown`.**

**- \*\*Status:\*\* "Under construction" needs dated evidence. "Operational" means most capacity is live.**

**- \*\*MW:\*\* `operational\\\\\\\_mw` is live today. Scope is 5 MW or more, or any AI-ready or AI-specific site. Never fit to benchmarks.**



**\*Benchmarks (context only)\***

**- \*\*Cushman and Wakefield H1 2026 operational MW:\*\* Mumbai 890, Chennai 214, Delhi NCR 183, Bengaluru 162, Hyderabad 151, Pune 133, Kolkata 22. The stated total is 1,789 but the seven add to 1,755.**

**- \*\*Other figures:\*\* datacentres.com has Mumbai at about 1,180 MW and Chennai at about 340 MW. The government figure is about 1,575 MW (Aug 2026). Telangana's release says over 300 MW.**

**- \*\*Gaps in the final file:\*\* Mumbai about −295 MW, Chennai +51, Hyderabad −80, Bengaluru −67, Pune about +24, Kolkata +16.**



**\*Policy and indicators\***

**- \*\*State rules:\*\* Andhra Pradesh 70% renewable (minister's statement, written order not found). Maharashtra 51% for green data centre parks (one source says 100%). Telangana up to one third under its 2016 policy. None found for Gujarat or West Bengal.**

**- \*\*National rule:\*\* the Renewable Consumption Obligation is 35.95% for 2026-27 (from secondary sources; confirm the Ministry of Power notification).**

**- \*\*Peak demand:\*\* unmet peak is about 0%. Peaks in Aug 2026 (MW) were Maharashtra 29,477, Gujarat 28,390, Andhra Pradesh 13,987, Telangana 17,288, West Bengal 12,745. The agent's file uses other periods (Andhra Pradesh 14,145 MW, Maharashtra 32,161 MW).**

**- \*\*Planned data centre MW as a share of state peak:\*\* Andhra Pradesh about 42.6%, Maharashtra about 17.4%, Telangana about 14.9%. These mix stages and bases, so use them only for ranking.**

**- \*\*State groundwater stage of extraction, 2024:\*\* Gujarat 54.2%, Maharashtra 53.0%, Telangana 45.9%, West Bengal 45.6%, Andhra Pradesh 29.8%, Tamil Nadu 74.3%.**



**\*Key project facts\***

**- \*\*Google Vizag hub:\*\* 1 GW combined with no per-parcel MW. Tarluvada is 266.6 acres, Adavivaram-Mudasarlova 160 and Rambilli (Anakapalli) 174.8. Groundbreaking was 28 Apr 2026, with a US$15 billion investment.**

**- \*\*Reliance Vizag:\*\* Vizianagaram district, 854.97 acres, order dated 20 May 2026, Rs 1.08 lakh crore. It includes a 15% water tariff subsidy for 10 years and a desalination study.**

**- \*\*AM AI Factory:\*\* 512 MW, Visakhapatnam district.**

**- \*\*RMZ-Colt:\*\* 1.25 GW, Rs 1.77 lakh crore.**

**- \*\*Sify:\*\* the investment conflict stands between Rs 15,266 crore and Rs 16,466 crore.**

**- \*\*Microsoft Hyderabad:\*\* region live since 6 Aug 2026, no MW disclosed.**

**- \*\*CtrlS Chandanvelly:\*\* announced Jan 2025, no construction evidence found.**

**- \*\*Reliance-Meta Jamnagar:\*\* 168 MW, release dated 10 Jun 2026.**

**- \*\*AdaniConneX Taloja:\*\* planned (CoreWeave 240 MW targeted for mid-2028), with 0 MW live in Navi Mumbai per company results.**

**- \*\*NTT NAV2:\*\* 43 MW operational per ICRA.**

**- \*\*TCS HyperVault Hyderabad:\*\* 264 acres, up to 1 GW.**

**- \*\*Odisha:\*\* Adani 1 GW (district conflict between Khordha and Cuttack/Naraj), SentraForge 120 MW (Puri) and HCLTech.**



**\*\*ETHICAL CONSIDERATIONS SURFACED\*\***



**\*Data sourcing and consent\***

**- \*\*Sources:\*\* all data came from public sources: government orders and parliamentary answers (CEA, CGWB via RBI), company releases and stock filings, rating reports (ICRA), news and trade press, and consultant summaries. No interviews or personal data were collected.**

**- \*\*Trackers:\*\* crowd-sourced and aggregated tracker sites (PeeringDB, DataCenterMap, Baxtel, Wikipedia) were allowed as leads only. Earlier agents misused them as primary evidence; this was corrected.**

**- \*\*Site restrictions respected:\*\* CGWB's compilation returned a "site disallows automated access" error. Claude did not work around it and asked Chetan to download the table manually. The agent also logged that CGWB, JJM and the National Power Portal need manual download.**

**- \*\*Copyright:\*\* evidence uses paraphrase, and the agent prompts limit excerpts to about 25 words.**



**\*Privacy and confidentiality\***

**- \*\*Dataset:\*\* it holds company, site and government data only. It contains no personal data about individuals.**

**- \*\*Researcher details:\*\* Chetan's name, roll number and background appear in the chat's memory notes, not in the dataset.**

**- \*\*Coordinates:\*\* they are blank because of tool limits, not by a privacy or security decision. Whether publishing exact facility locations raises a security concern was not discussed.**



**\*Social and environmental impact\***

**- \*\*Water and energy:\*\* the project's purpose is to judge energy and groundwater stress. The Andhra Pradesh pipeline is about 6 GW, roughly 43% of state peak demand, and several target districts have stressed groundwater. Reliance's Vizag order gives a 15% water tariff subsidy for 10 years, and company claims of seawater, desalinated or zero-water cooling are recorded as claims.**

**- \*\*Land and clearance:\*\* land allotments include acreage handed to Google's subsidiaries and Reliance, and Adani's Odisha parcel (about 250 acres). A clearance controversy for the Vizag hub ("Category B", from Chetan's earlier brief) appeared only in notes. This chat did not examine land disputes, displacement, community objections or legal challenges.**

**- \*\*Unresolved district:\*\* the Adani Odisha district is disputed between Khordha (official clearance lists) and Cuttack/Naraj (other reports).**



**\*Use of AI-assisted tools and how errors were handled\***

**- \*\*Errors seen:\*\* multiple AI agents produced fabricated or inflated data, including URLs and dates that looked plausible but were wrong, 313.5 MW of unsupported "live" capacity, and numbers fitted to benchmarks.**

**- \*\*My own mistakes:\*\* Claude's own earlier mistakes were also corrected (the STT 600 MW row, an AIRAWAT row, a wrong "MW not found" for STT, and misjudging a file from a report's narrative).**

**- \*\*Safeguards:\*\***

&#x20; **- Staged work with stop points.**

&#x20; **- A URL-provenance rule.**

&#x20; **- Fixed source tiers.**

&#x20; **- Independent review in separate sessions, with code checks on every delivery.**

&#x20; **- Live-search spot-checks of rows and links.**

&#x20; **- Versioned files with change logs and no overwriting.**

&#x20; **- A ban on self-certification.**

**- \*\*Still unmet:\*\* Chetan has not yet opened the 15 random links.**



**\*Transparency about limits, uncertainty and unverifiable claims\***

**- \*\*Labelling:\*\* rows are labelled with a verification status. Company claims are marked "claimed" or "proposed". Conflicting values are recorded, not hidden (Sify investment, Adani district, CtrlS 150 vs 370 MW).**

**- \*\*MW bases:\*\* MW is split by IT load versus facility load.**

**- \*\*Evidence limits:\*\* the agent saw only search snippets, not full pages. District evidence is a portal page that does not name villages. Evidence paraphrases are templated.**

**- \*\*Remaining blanks:\*\* all coordinates and all district water and electricity fields are empty.**

**- \*\*No fitting:\*\* benchmark gaps are reported as gaps.**



**\*Conflicts of interest and source bias\***

**- \*\*None stated:\*\* no conflicts of interest or funding were raised in this chat.**

**- \*\*Source bias:\*\* operator pages and state-government statements are self-reported and promotional. They were counted as "primary" but are not independent, which the verification labels cannot fully fix.**



**\*Integrity safeguards built into the methodology\***

**- \*\*Evidence and counting:\*\* two independent sources or one primary source per key field. No nested rows in totals. Separate live and planned capacity.**

**- \*\*Scope and recording:\*\* a 5 MW scope rule, with excluded sites recorded with reasons. Page dates recorded only if visible.**

**- \*\*Verification:\*\* an evidence log, a URL registry and a gap table computed by code.**



**\*\*WHAT TO IGNORE\*\***

**- Old datasets and summaries (`facilities\\\\\\\_merged\\\\\\\_v2.json`, v1 and v2 of the agent datasets) and the first-round audits.**

**- All "0 errors", "100%" and "verified" self-claims by any agent.**

**- The 20.5 GW and 19 GW pipeline headlines.**

**- The "STT 600 MW" row (it was CtrlS) and AIRAWAT (a supercomputer).**

**- Wikipedia market-total rows.**

**- AWS and Google per-site MW splits and the fitted benchmark explanations.**

**- Calculations of data centres' own water use (Chetan wants normal human and local water use).**

**- The early research-framing options A–D (never chosen).**

**- Repeated column explanations and further verification rounds, unless he asks.**



##### **Context from rajchetan.offical@gmail.com | DISSERTATION 3**





\*\*TASK\*\*



Chetan is a non-technical TISS student (B.S. Analytics and Sustainability Studies). His dissertation asks whether India's AI data centre expansion is sustainable. This chat was his working session for the data and evidence side of that project.



1\. Build a sourced list of data centre sites in India (state, district, status, live and planned MW, power and cooling facts).

2\. Collect district- and state-level electricity, grid and water indicators as inputs to a location risk matrix. Scoring is not my task; only sourced inputs are.

3\. Get coordinates for the sites for GIS work.

4\. Run two literature syntheses, one on water and one on energy and the grid, as Excel workbooks with page-cited evidence.

5\. Plan a web dashboard that maps every data centre over an India-wide district groundwater map.



\*\*CURRENT STATE\*\*



Files are in `/mnt/user-data/outputs/` (my sandbox; the chat summaries don't show them, so re-upload if needed). The literature workbooks sit on his own computer under `Desktop/SEM 7/Dissertation/01\\\\\\\_Literature\\\\\\\_Review/` (subfolders `Water/` and `Energy/`).



\*Data centre list (done, with caveats)\*

\- `data\\\\\\\_centres\\\\\\\_final\\\\\\\_v1\\\\\\\_2.csv/.json`: 118 rows (114 campuses plus 4 nested phases, CORE01a/b/c and CORE02a), 14 states, 29 district groups, 2 rows with no district (CORE16, CORE119).

\- Live MW: 1,380.54 IT load and 37.0 facility load. Planned MW: 9,362.9 IT load and 9,141.0 facility load. Bases are never mixed. Phases are excluded from sums. I checked the sums by code.

\- Evidence: 28 rows with 2+ independent sources, 40 primary, 49 partial, 1 unverified. Describe it as "sourced, with confidence levels", not "fully verified".



\*Groundwater (done; one human check open)\*

\- `cgwb\\\\\\\_2025\\\\\\\_district\\\\\\\_groundwater\\\\\\\_29.tsv`: all 29 districts, from the CGWB GWRA 2025 Annexure II, in ham (1 ham = 10,000 m³). Extraction was done by an AI from the PDF; I checked component sums and stage ratios by code.

\- The district category is my own derivation from the stage of extraction \[I], using CGWB thresholds (up to 70 safe, to 90 semi-critical, to 100 critical, above 100 over-exploited).

\- Over-exploited: Gurugram 194.6%, Bengaluru Urban 177.3%, Bengaluru Rural 146.8%, Chennai 121.7%, Indore 118.0%, Gandhinagar 111.3%, Sonipat 108.7%, Gautam Buddha Nagar 105.2%.

\- Net availability can be positive when the stage is above 100% (my guess \[I]: summed over blocks with room).

\- `cgwb\\\\\\\_2025\\\\\\\_block\\\\\\\_categories\\\\\\\_29\\\\\\\_districts.tsv`: block counts by category from his JSON. State fact sheets are state-level only (my early mistake).

\- \*\*Open:\*\* he must check three numbers against the PDF: Gurgaon (p.182, 194.60%), Chennai (p.198, 121.72%), Raigad (p.189, 18.44%).



\*Tap water (done)\*

\- `jjm\\\\\\\_tap\\\\\\\_coverage\\\\\\\_28\\\\\\\_districts.tsv` (Jal Jeevan Mission dashboard, as on 28 Oct 2026; rural households only). Mumbai Suburban and Chennai are not in the table (fully urban: not applicable, not zero). South East Delhi was not collected. Use this file's state percentages, not the live J17 page.



\*Energy (state level)\*

\- No public district-level hours of supply exists; a stated limitation.

\- `state\\\\\\\_power\\\\\\\_supply\\\\\\\_hours\\\\\\\_FY2023-24.tsv` (Rajya Sabha Q153, 3 Feb 2025, PDF p.32). Rural hours: UP 18.1, Haryana 19.4, Karnataka 21.4, Chhattisgarh 21.6, Telangana 21.9, Bihar 22.2, MP 22.6, Odisha 23.4, WB 23.4, TN 23.5, AP 23.6, Gujarat 23.7, Maharashtra 23.8. Delhi rural is `\\\\\\\*` (unexplained, blank). The FY2025-26 state table was not found.

\- `state\\\\\\\_energy\\\\\\\_inputs\\\\\\\_v3.tsv`: CEA Energy and Peak reports (Revised, Aug and Apr–Aug 2026). Peak demand (MW): AP 13,967; Bihar 9,591; Chhattisgarh 6,023; Delhi 7,660; Gujarat 28,400; Haryana 14,895; Karnataka 16,894; MP 13,390; Maharashtra 29,497; Odisha 7,347; TN 20,721; Telangana 17,291; UP 31,486; WB 12,695. UP has 190 MW unmet at the August peak (0.6%; April–August 1.6%). Elsewhere the figure is about zero. State-level supply is adequate, so stress is local (feeders and substations), which the reports don't show.

\- It also holds data centre renewable rules for 5 states, from secondary sources with orders not read: AP at least 70% (minister's statement), Maharashtra 51% (one source says 100%), Telangana one third (2016 policy), Gujarat and WB none found. National renewable consumption obligation: 35.95% for 2026-27. Rules for 9 states are still unresearched. The latest grid batch mentions a 2026 Gujarat policy and a Haryana policy (gazette 27 May 2026, seen only on an aggregator).



\*Grid evidence (all 29 districts covered; mostly unverified)\*

\- Built through web-search AI batches, a combine prompt, and my checks. Files: `grid\\\\\\\_A\\\\\\\_all\\\\\\\_v1.tsv` (serving DISCOMs and transmission companies, 29 districts), `grid\\\\\\\_B\\\\\\\_all\\\\\\\_v1.tsv` (29 evidence rows), `grid\\\\\\\_C\\\\\\\_all\\\\\\\_v1.tsv` (23 DISCOM ratings, 14th Integrated Rating, FY 2024-25), `grid\\\\\\\_evidence\\\\\\\_maharashtra\\\\\\\_tn\\\\\\\_checked\\\\\\\_v1.tsv`, and the cleaned versions.

\- The AIs opened 0 pages; everything is snippet-only. Tiers were standardised (mixed tiers use the lowest; Scribd, blogs, aggregators and vendor pages are \[T]).

\- \*\*Confirmed by me:\*\* MERC approved a 400/220 kV GIS substation at Ambernath (Palava, Thane) for Lodha's data centre park, with about 1,450 MW connectivity granted and 1,500 MW more under consideration (trade press, June 2026; I did not read the MERC order). AEML grade A+ (99.75, rank 3).

\- \*\*Unconfirmed:\*\* MSEDCL grade C, TNPDCL B-, TGSPDCL C- (no score). APCPDCL "B" at 67.53 looks wrong (UHBVN A at 66.32, South Bihar A at 67.37). BRPL "B-#" is a regulatory override.

\- Districts with no grid evidence: Indore, Patna, Raipur, Gautam Buddha Nagar, Hooghly, North 24 Parganas, Ranga Reddy.

\- A separate agent (his Google Sheet "India\_AI\_DataCentre\_Dissertation\_Master"; I read only the README tab) computes risk scores. I advised: Gurugram is served by DHBVN (A, 74.44), Panchkula and Sonipat by UHBVN (A, 66.32); the Red Card override applies only to MSEDCL, TNPDCL and BESCOM; do not use `DC\\\\\\\_water\\\\\\\_demand\\\\\\\_ham` in scoring; leave Chennai's `compounded\\\\\\\_flag` unresolved.

\- The `grid\\\\\\\_\\\\\\\*\\\\\\\_all` files are de-duplicated (the README tab describes them as raw; that is wrong).



\*Merged district sheet\*

\- `district\\\\\\\_inputs\\\\\\\_combined\\\\\\\_v3.tsv` (supersedes v1 and v2): 29 district rows plus 2 no-district rows. It has groundwater, block counts, JJM, state power hours, data centre MW (`dc\\\\\\\_` columns), serving DISCOMs, transmission company, 14th rating, and grid evidence counts. Visakhapatnam carries Google's 1,000 MW hub (which also spans Anakapalli).



\*Coordinates (38 of 114 campuses usable)\*

\- `coordinates\\\\\\\_accepted\\\\\\\_v2.tsv`: 7 checked (Plus Codes or official filings, decoded by me), 15 OpenStreetMap (Overpass export `export.geojson`, community-mapped), and 16 Google Places points from an AI batch (operator matched).

\- Rejected: CORE20 (pin at the NAV2 site), CORE34 (Manapakkam vs Neervallur, Kanchipuram district), CORE57 (135 m from CORE56). Unverified candidates not used: CORE35, CORE77. Not usable: CORE72's printed Sify coordinates (conflict) and CORE71 (hobbyist atlas).

\- `coordinate\\\\\\\_gaps\\\\\\\_v1.tsv`: 76 campuses without points (36 operational, 11 under construction, 29 announced or planned). Group C sites mostly have no public pin and stay at district level.

\- A Plus Code reply for the Vizag area was decoded by me but not yet added: CORE01 Tarluvada W857+7X decodes to about (17.908, 83.315) from the Google hub's pin; the Rambilli "Vizag Data Centre Park" FW7V+4P decodes to about (17.463, 82.944). Treat both as candidates only (the AI's tool hid raw coordinates; it gave Plus Codes).

\- The coordinate-fill prompt for the remaining states has been written. The AP batch returned almost nothing. Uttar Pradesh, West Bengal, Telangana and Karnataka were suggested first.



\*Dashboard plan (not started)\*

\- He chose Option B: a district-level map of India shaded by groundwater stage of extraction, with one dot per data centre (sized by MW, coloured by status) and a credibility label on every dot ("site point checked", "community-mapped", "Google Places operator matched", "district only, position approximate").

\- Needed from him: the district boundary file (he says he has it; it hasn't reached me; simplify to a small GeoJSON for a page limited to 16 MB) and the full CGWB Annexure II for all districts (extraction prompt written, three or four batches by state). I will build the name crosswalk (Gurgaon/Gurugram, Khurda/Khordha, and so on) and a code check that every dot sits inside its stated district. Rows with no district get no dot.



\*Water literature workbook\* (`water\\\\\\\_datacentre\\\\\\\_literature\\\\\\\_synthesis\\\\\\\_v1.xlsx`; 13 sheets; built by an external agent in stages)

\- 14 sources: P01 to P10 (Mytton 2021; Siddik 2021; Li et al.; de Vries-Gao 2026; Rosa et al. (ES\&T); Masanet preprint; CEEW Feb 2026; Planet Tracker 2025 Asia (P08, from a 3-page PDF with the table body missing); Planet Tracker Sept 2024; Baringa Nov 2025), plus web press P11 to P14 (Down To Earth ×2, LiveLaw, OpenCity). P12 and P14 are secondary; P13 uses the same CGWB 2025 data as his dataset.

\- The agent reported 215 Extraction rows plus India\_Press rows, with mechanical checks (quotes found on pages, formulas recalculated, numbers traced). My review caught outside-knowledge claims, a wrong author name, thresholds the papers don't print, and an agent-generated "published" banner on web PDFs. Fixes were applied.

\- \*\*Still open:\*\* I suspect the "Published by ... | year" banners on P08, P09 and P11 to P14 were added when the PDFs were generated. I advised DATE NOT PRINTED and "cite section and paragraph, not page" for web sources. I have not seen the workbook, and the spot-check is pending.



\*Energy literature workbook\* (`energy\\\\\\\_datacentre\\\\\\\_literature\\\\\\\_synthesis\\\\\\\_v1.xlsx`; 16 sheets)

\- Built unattended in 7 stages. Sources: E01 Masanet 2020; E02 LBNL 2024; E03 IEA Energy and AI 2025; E04 de Vries-Gao 2025; E05 de Vries-Gao 2026; E06 JLARC 598; E07 E3 for JLARC; E08 CEEW; E09 FSR Global; E10 Ireland CRU decisions; E11 Ministry of Power (Rajya Sabha UQ 956, answered 27.07.2026) and Business Standard (29 Jul 2026); E12 ThePrint; E13 and later: trade press and CSO Ireland.

\- After my review, it added Lineage\_Groups (merging sources with shared authors, commissioning links or shared data, such as E01 and E02, E04 and E05, E06 and E07, and CEEW with FSR Global), moved press sources to illustration only, corrected the Ministry of Power date, and added a side-by-side table of India's projections.

\- India projections (different measures; do not compare them as the same thing): 26.3 GW additional load by FY32 (Ministry of Power, via the CEA's 20th survey; earlier March 2026 ministry figure 13.56 GW); above 13.6 GW by 2032 and 16.4 GW by 2040 (a CEA report as reported by ThePrint); FSR Global's 2030 installed capacity scenarios (4 to 5, 8 to 10, and 12 to 17 GW).

\- \*\*Ashburn test:\*\* Chetan's claim ("about 50 million square feet could not get electricity and sat idle") is NOT SUPPORTED by any source. What the sources show: 2022 transmission constraints in eastern Loudoun that delayed power for new projects (about 26 million sq ft existing and about 5 million in development at that time); 56.5 million sq ft built or under construction by 2026; colocation vacancy 0.2%; waits of 3 to 7 years for new connections (trade-press figures). The Ashburn claim's origin is recorded as "supplied by the user; not found in any attached source".

\- \*\*Small fixes still pending (my last message):\*\* move the renewable-feasibility row out of the projections table; split the Mumbai and Southern Region row; reword PAT-0005 and PAT-0006 as separate US/Ireland and India findings; quote printed dates for E11\_S and E12.



\*To-do list\*

1\. Chetan: groundwater 3-number check; open about 15 data centre links; check the 23 DISCOM grades against the PFC 14th Integrated Rating; upload the boundary file and the all-district groundwater extraction; pick key sites for coordinates; fix the web-PDF dates.

2\. Me: spot-check both workbooks if uploaded (about 15 rows against the PDFs, independence of patterns, Link\_to\_My\_Dataset); state data centre rules for 9 states; limitations list for the dissertation; build the dashboard; add the coordinates that come back.



\*\*KEY CONTEXT\*\*



\*Chetan's preferences\*

\- One step at a time with explicit confirmation; plain language, short answers, and the reason a fix works.

\- Copyable output (TSV, JSON, markdown for Excel); distinct file names and the exact destination for each file.

\- Cost-conscious and tired of long verification loops; not technical.

\- Tags: \[S] sourced data, \[I] my inference.

\- Workflow: I write prompts; he runs them in other AI agents (web-search AIs, PDF readers, a local agent with Excel), uploads the outputs, and I check them by code and with my own search before accepting.



\*Data rules\*

\- Source tiers: \[P] operator pages or releases, filings, government orders, regulators; \[S] major news, trade press, rating reports, consultants; \[T] trackers, blogs, aggregators, Scribd, vendor pages (never sole support).

\- URLs only if a tool returned them; homepages are not evidence; page dates only if visible.

\- Precision tiers: Exact site (about 100 m), Plot or village (about 1 km), Locality or industrial area (about 5 km), City centroid, District only, Unknown.

\- `operational\\\\\\\_mw` means live today; scope is 5 MW or more, or any AI-ready site.



\*Benchmarks (context only)\*

\- Cushman and Wakefield H1 2026 operational MW: Mumbai 890, Chennai 214, Delhi NCR 183, Bengaluru 162, Hyderabad 151, Pune 133, Kolkata 22 (stated total 1,789; the seven add to 1,755). Gaps against the final file: Mumbai about −295, Chennai +51, Hyderabad −80, Bengaluru −67, Pune about +24, Kolkata +16.

\- Planned MW as a share of state peak is to be recomputed from the revised peak figures; use for ranking only.



\*Key project facts\*

\- Google Vizag hub: 1 GW combined (Tarluvada 266.6 acres, Adavivaram-Mudasarlova 160, Rambilli 174.8); groundbreaking 28 Apr 2026. Reliance Vizag: Vizianagaram, 854.97 acres, order 20 May 2026. AM AI Factory 512 MW. RMZ-Colt 1.25 GW. Reliance-Meta Jamnagar 168 MW (10 Jun 2026; desalinated seawater cooling). TCS HyperVault Hyderabad 264 acres, up to 1 GW. STT Hyderabad up to 100 MW (MoU 18 Jan 2025). CtrlS Chandanvelly: no construction evidence. L\&T Panvel: only the 2 MW pilot is confirmed. AdaniConneX Taloja planned (CoreWeave 240 MW, mid-2028). Odisha: Adani 1 GW (district conflict, Khordha vs Cuttack/Naraj), SentraForge 120 MW (Puri). CtrlS rows total 162.4 MW against ICRA's 150 MW company-wide.



\*Mistakes of mine to remember:\* I assumed the CGWB state fact sheets held district tables (they don't); I quoted live J17 JJM state percentages that differ from the file; I described the water workbook's P08 as "NOT AVAILABLE" before he found a partial file.



\*\*ETHICAL CONSIDERATIONS SURFACED\*\*



\*Data sourcing and consent\*

\- Almost all data is public government or institutional records: CGWB groundwater assessment, Jal Jeevan Mission dashboard, CEA peak and energy reports, Parliament answers, PFC DISCOM ratings, MERC and CRU decisions, JLARC. There are no human participants and no personal data. Consent was not required, but source and licence terms were not discussed in this chat.

\- Aggregated and republished data was used with care: OpenCity republishes CGWB data (cited with CGWB as the primary source, and not used as independent confirmation); data tracker sites are tier \[T] and can never be the sole support.

\- Crowd-sourced data: OpenStreetMap points (community-mapped) are rated lower than checked points and labelled as such. OSM attribution and licence terms were not discussed here (flag for checking before publication).

\- Google Maps and Places data came through an AI tool. Coordinates were accepted only when they matched the operator and facility name and passed my checks; seven AI-returned points were rejected or held back.

\- Some primary files could not be fetched by me (sansad.in, the CGWB site, the CEA PDFs), so Chetan downloaded them. Web pages saved as PDFs have no stable page numbers; he was advised to cite section and paragraph, plus URL and access date.



\*Privacy and confidentiality\*

\- No personal data was collected. Site locations are corporate facilities. For sites without a verified point, the dashboard plan uses district-level dots and labels them "position approximate". His brief said exact locations are not necessary, so precision is intentionally limited and disclosed.

\- Operator data such as water use is commercially confidential and largely undisclosed (a finding in the literature, and why the dataset uses local water indicators instead of operator water use).



\*Social and environmental impact surfaced in the work\*

\- Land and approvals: large land allotments (for example Reliance Vizag 854.97 acres under a government order, Google's Vizag parcels), a 15% water tariff subsidy for Reliance Vizag, and an Odisha site whose district is disputed (Khordha vs Cuttack/Naraj). The dataset records these as stated and flags conflicts instead of resolving them.

\- Water: data centres sit in or near districts where groundwater use is already above 100% of the extractable resource (Gurugram, Bengaluru, Chennai, Indore, Gandhinagar, Sonipat, Gautam Buddha Nagar). The groundwater and tap-water indicators are local, normal-use measures, not data centre consumption. JJM covers rural households only.

\- Electricity and ratepayers: grid constraints around Ambernath (Thane), CEA's warning to states about data centre load, and (in the literature) the risk that new grid costs fall on other ratepayers.

\- Community objections, legal challenges and displacement appeared only in search-result snippets (for example residents objecting to Virginia transmission lines, a county lawsuit over notice rules, homes close to data centres, Bengaluru water complaints). They were not analysed as part of the dataset, and I did not examine any displacement.

\- The user's Ashburn claim ("50 million sq ft sitting idle") was checked and found unsupported, so it will not be repeated as fact.



\*Use of AI-assisted and automated tools, and how errors were handled\*

\- Several external AI agents built and "fixed" the data centre dataset in earlier sessions. Problems seen included invented URLs and dates, homepages and trackers treated as evidence, totals fitted to consultant benchmarks, auditors editing the data they audited, and self-certified "0 errors". Handling: strict source tiers, URLs only from tool output, MW never fitted to benchmarks, my own code checks, and distrust of agents' "verified" claims.

\- In this chat, I verified AI outputs before accepting them. Examples: arithmetic and stage-ratio checks on the AI-extracted groundwater table; Plus Code decoding and degrees-to-decimal checks on coordinates; checking an AI's "found" coordinates and finding they only echoed numbers in a search link; rejecting points in the wrong district or on the wrong site; confirming Ambernath and AEML claims with my own search; catching rating inconsistencies.

\- The AI grid and rating batches were snippet-only (no pages opened). They are labelled so, and unconfirmed grades are marked unverified.

\- The literature workbooks were built by an AI agent with code checks (quote appears on the cited page, formulas recalculated, numbers traced). I told Chetan that these checks show a quote exists on a page and a number is traced, not that an interpretation is fair, and I asked him to upload the workbook and PDFs for a human-style spot-check. Issues the review caught: outside-knowledge facts in synthesis sheets (for example grid mix and litre-per-kWh figures not in any paper), a wrong author name, stress thresholds not printed in the papers, derived ratios not labelled as derived, sources counted as independent when they shared authors, commissioning or data, trade press counted as support, and a wrong date on a government document.

\- Dates and page numbers: banners reading "Published by ... | year" appear to have been added to web-print PDFs, so they are not used as dates; page numbers for web-print PDFs are only locators in his file.

\- I (Claude) made mistakes too (see above), and also could not open several sources myself.



\*Transparency about limitations, uncertainty and unverifiable claims\*

\- Coordinates: 38 of 114 campuses; others at district level. Power hours are state-level and FY2023-24 only. District net groundwater availability can be positive above 100% stage (unexplained). Tap coverage is rural only. The district category is derived \[I].

\- Planned MW mixes stages (announced, approved, under construction); IT and facility load bases are kept separate; known capacity conflicts (CtrlS, AdaniConneX, NTT NAV2) are accepted and flagged; 49 data centre rows are only partly verified.

\- Grid evidence is mostly press and snippet-only; district-level grid headroom data is not public. The ratings for MSEDCL, TNPDCL, TGSPDCL and most others are unverified. India's projections for data centre demand conflict (13.56 vs 26.3 GW by FY32) and are shown side by side with their dates, not merged.

\- Blank or "NOT REPORTED / NOT AVAILABLE" is used instead of guessing (for example Delhi's rural hours `\\\\\\\*`, a missing P08 table, CGWB-derived press not used as confirmation).

\- The `\\\\\\\[I]` tag separates my inferences from sourced facts; "verified" is avoided unless a code check produced it.



\*Potential conflicts of interest\*

\- Operator pages count as primary but are not independent of the operator. Industry-linked and commercial sources (consultancies such as Baringa, JLL, CBRE and Cushman \& Wakefield; trade press that depends on industry; funding statements) were flagged as non-independent or secondary. One news item disclosed that a utility is a donor to the outlet.

\- Think-tank and NGO sources (CEEW, Planet Tracker, FSR Global, Friends of the Earth) have their own positions; the literature workbooks mark source type and use independence ("lineage") checks to avoid double counting.

\- No conflict of interest for Chetan or me was discussed in this chat.



\*Accuracy and integrity safeguards built into the methodology\*

\- Source tiers \[P]/\[S]/\[T]; URLs only from tools; no homepage evidence; page dates only if visible.

\- Code checks: sums and ratios, Plus Code decoding, district and proximity checks, de-duplication, quote-on-page tests, formula recalculation, number tracing; independent spot-checks by Chetan (three groundwater numbers, 15 data centre links, DISCOM grades).

\- Excerpt cap of 25 words with paraphrase, which also limits copying of copyrighted papers.

\- Backups at every stage of the workbooks; decision and progress logs in the energy workbook.

\- Rejected, downgraded or flagged items are listed rather than deleted (for example CORE20, 34, 57, 35, 77, 71 and 72).



\*\*WHAT TO IGNORE\*\*

\- Old datasets and summaries (`facilities\\\\\\\_merged\\\\\\\_v2.json`, agent v1 and v2 files, first-round audits) and any "0 errors", "100%" or "verified" self-claims by any agent.

\- The 20.5 GW and 19 GW pipeline headlines; the "STT 600 MW" row (it was CtrlS); AIRAWAT; Wikipedia market-total rows; AWS and Google per-site MW splits; the Kolkata "22.4 MW before CtrlS" note.

\- Data centre water-use calculations, including `DC\\\\\\\_water\\\\\\\_demand\\\\\\\_ham` (he wants normal human and local water use).

\- Superseded files: `district\\\\\\\_inputs\\\\\\\_combined\\\\\\\_v1/v2`, `state\\\\\\\_energy\\\\\\\_inputs\\\\\\\_v1/v2`, `coordinates\\\\\\\_so\\\\\\\_far\\\\\\\_v1.tsv`, `coordinates\\\\\\\_maharashtra\\\\\\\_batch1.tsv`, raw `grid\\\\\\\_A/B/C` files with duplicates, and earlier AI coordinate batches for Tamil Nadu and Telangana.

\- Unverified coordinates for CORE35, CORE77, CORE72, CORE71, CORE20, CORE34 and CORE57, and the old Nominatim points.

\- News-based power figures, the JJM live J17 state table I quoted early, and the early research-framing options (A to D).

\- Repeated prompt drafts, the agent's loop and stuck runs, and further verification rounds unless he asks.



##### **Context from raxagain13@gmail.com | DISSERTATION 2.1**



**TASK:**

**This chat supports Chetan's India-based dissertation on data centres (energy demand, supply, regulation, water). Its jobs were:**

**1. Document the dataset `facilities\\\\\\\_merged\\\\\\\_v2.json`.**

**2. List the variables that decide where new large data centres (hyperscale or AI, similar energy draw) are sited.**

**3. Map state-level policy and regulation, with the regulatory angle as the priority.**

**4. Deep-dive Andhra Pradesh (AP) and Gujarat, and compare them with states that have few or no large data centres.**

**5. Add a "why here" rationale column to 22 facilities.**

**6. Write a concise two-page note on location reasons and on how seriously companies treat sustainability (green energy, water).**



**CURRENT STATE:**

**- \*\*Memory import (`/import-memory`):\*\* I read the dissertation context brief and proposed filing six memory files. I proposed leaving out the roll number, URLs, working-style rules and general definitions. The user never confirmed, so nothing was written.**

**- \*\*README:\*\* `README\\\\\\\_facilities\\\\\\\_merged\\\\\\\_v2.md` was created and delivered. It covers 89 records and 23 fields.**

&#x20; **- Record types: 56 facility, 11 excluded, 10 state\_rollup, 8 child, 3 programme, 1 national\_rollup.**

&#x20; **- Capacity gaps: 74 of 89 records have no operational MW and 48 have no ultimate MW.**

&#x20; **- Sums: summing only facility rows with `sum\\\\\\\_ok = true` gives 94 MW operational and 7,081.4 MW ultimate. Treat these as indicative, because `cap\\\\\\\_basis` varies and the figures are not like-for-like.**

&#x20; **- Sparse fields: only 7 records have `power\\\\\\\_procurement` and 6 have `cooling\\\\\\\_water`.**

&#x20; **- Inferred meanings: the file has no schema, so the `sum\\\\\\\_ok` meaning, the F/N ID series and the parent/child semantics are inferred.**

&#x20; **- Parent/child quirks: `F39` is typed `child` but has no parent, and `F33` contains its own parent `F32`.**

**- \*\*Siting variables:\*\* grouped as power, water and climate, land and approvals, connectivity and market, policy and regulation, risk and economics.**

**- \*\*State policy landscape, lever matrix and primary-text pulls:\*\* delivered, with details below.**

**- \*\*Rationale column:\*\* delivered as tab-separated text for the 22 rows. Each bullet is tagged \[S] (sourced from the row data or earlier research) or \[I] (my inference).**

**- \*\*Two-page writeup:\*\* delivered. It gives six location reasons and a verdict that green power is moderate and mostly pledges, while water is weak.**

**- \*\*Explanations:\*\* I also explained why subsea cables matter, what an anchor tenant is, and why companies build at specific sites.**

**- \*\*Open items:\*\***

&#x20; **1. Confirm or decline the memory import.**

&#x20; **2. Pull the primary policy texts for Odisha, Haryana and Rajasthan.**

&#x20; **3. Fill the "not found" cells in the lever matrix.**

&#x20; **4. Verify the AP 70% renewable rule in a government order (GO).**

&#x20; **5. Verify how Gujarat measures its 51% and its penalties.**

&#x20; **6. Find the outcome of the AP High Court hearing on 5 October 2026.**

&#x20; **7. Get the Telangana policy PDF.**

&#x20; **8. Check whether West Bengal's policy was extended.**



**KEY CONTEXT:**

**\*\*User preferences\*\***

**- Concise, simple language, and the least computationally heavy output format.**

**- Plain text or tab-separated text that the user converts to Excel themselves.**

**- Emphasis on the regulatory aspect, and on new big data centres rather than small colocation.**

**- The user referred to an "Objective 2" (regulatory analysis, as I understood it; check this against the brief).**



**\*\*Central layer\*\***

**- No dedicated central law or national data-centre policy with uniform benchmarks.**

**- Environmental clearance applies to data centres only as building or township projects (above 20,000 sq m built-up, or 50 hectares or more), assessed on footprint rather than power or water.**

**- Budget 2026-27 gave a tax holiday to 2047 for eligible foreign cloud providers.**

**- The central transmission utility issued a General Network Access (GNA) procedure in April 2026.**

**- CEA's resource adequacy plan projects 458.7 GW peak demand by 2035-36.**



**\*\*Gujarat\*\***

**- Viksit Gujarat Data Center Policy 2026-29, effective 9 July 2026 and notified 7 August 2026. Target 7.5 GW and Rs 6 lakh crore, with Dholera as the hub.**

**- Incentives apply from 150 MW IT load and are available until 7.5 GW is installed. Re 1 per unit for 20 years, 100% electricity-duty reimbursement for 20 years, and a 2.5% capital subsidy (Dholera only).**

**- Interest subsidy up to 4% for 10 years, capped at Rs 25 crore a year. Total assistance is capped at 75% of eligible investment. 20% capital subsidy for desalination.**

**- Condition: at least 51% renewable power. Dual feeders, essential-service status and help obtaining a distribution licence.**

**- Proposals reached roughly 10 GW in July and nearly 17 GW by September, against a 7.5 GW target.**

**- Installed-capacity claims conflict (69 GW versus about 74 GW).**

**- Critique: the policy does not explain how generation, storage and transmission will match the demand.**



**\*\*Andhra Pradesh\*\***

**- DC Policy 4.0 (2024-29), with custom packages through the Economic Development Board. Target 6 GW.**

**- Google/Raiden package of about Rs 22,000 crore: Re 1 per unit for 15 years, exemptions from electricity duty, transmission and RE cross-subsidy charges, a 25% water-tariff subsidy for 10 years, a land rebate, a capital subsidy and SGST reimbursement.**

**- Reliance package of about Rs 19,100 crore against about Rs 1.08 lakh crore of investment. AM AI Factory (512 MW) approved 22 August 2026.**

**- Deemed distribution licence (G.O. Ms No. 32, 22 April 2026) for projects of 300 MW or more. Contested by the Human Rights Forum.**

**- Vizag clearance: filed 24 April 2026 as Category B2 under the building and construction category. The site is 0.86 km from the Kambalakonda sanctuary and includes 160 acres of temple land. PIL No. 137 of 2026, plus reported National Green Tribunal cases.**

**- The High Court directed the state on 24 August to ensure all clearances and declined a stay. The 5 October hearing outcome was not found.**

**- Vizag district has the state's lowest groundwater availability.**

**- Water plan: Polavaram water to Visakhapatnam.**

**- On 25 September 2026 the IT minister said at least 70% of data-centre energy must be renewable. This is a ministerial statement, not yet seen in a GO, and it corrects my earlier "no RE share found".**



**\*\*Maharashtra\*\***

**- Green park framework of October 2024, amended in June 2026: parks raised from 3 to 20, statewide, green requirement cut from 100% to 51%.**

**- Re 1 per unit for 10 years at the Rs 30,000 crore investment tier. Ambition of 30 to 40 GW.**



**\*\*Uttar Pradesh\*\* (read from G.O. 536/78-2-2026/E-105226, 9 July 2026)**

**- Five years, replacing the 2021 policy. Target 2 GW or more and over Rs 2 lakh crore.**

**- A park is 40 MW or more and a unit is above 2 MW and below 40 MW.**

**- Park incentives: interest subsidy of 60% for 7 years, capped at Rs 10 crore a year and Rs 50 crore overall. Boosters add up to Rs 10 crore each for AI compute and green performance, about Rs 70 crore in all.**

**- Unit incentives: 7% capital subsidy capped at Rs 20 crore, plus a 10-year electricity-duty exemption.**

**- Wheeling and transmission relief of 50% (75% for in-state RE) for 25 years, limited to the first 8 parks or 2 GW.**

**- Renewable share is only encouraged (50% by 2030).**

**- The AI booster needs 700 FP64-grade units.**

**- Projects above 500 MW get discretionary packages, and Cabinet approves those above Rs 200 crore.**

**- No mandatory reporting.**



**\*\*Other states\*\***

**- \*\*Karnataka:\*\* Sustainable DC Policy 2026-31, targeting 1 GW IT load by 2031, PUE-linked incentives, a resource heat map and a Rs 1,300.45 crore budget.**

**- \*\*Telangana:\*\* 2016 policy, target 5 GW by 2029, a planned 1,500-acre data-centre city, and a 1,500 MW Shadnagar load listed for FY2031-32. Primary text not found.**

**- \*\*Tamil Nadu:\*\* 2021 policy covered data centres incorporated until 31 March 2026, with 30% RE and a 5-year electricity-tax subsidy. No successor found.**

**- \*\*West Bengal:\*\* 2021 policy from 6 September 2021, valid five years, so it nominally lapsed around 6 September 2026 (my arithmetic). Only stamp-duty and electricity-duty relief, no renewable condition or tariff subsidy. A new policy is reportedly being drafted. The body text comes from a mirror site.**

**- \*\*Rajasthan:\*\* 2025 policy with a Rs 20,000 crore target and 100% waiver of banking, transmission and wheeling charges.**

**- \*\*Haryana:\*\* policy of 27 May 2026, with a 20% capital subsidy capped at Rs 25 crore per hyper unit and custom packages for mega projects.**

**- \*\*Odisha:\*\* 2022 policy, a 20% capital subsidy capped at Rs 25 crore per unit.**

**- \*\*Bihar:\*\* spare power for 9 to 12 mid-sized data centres, but no cluster, workforce or global capability centre ecosystem.**

**- \*\*Chhattisgarh:\*\* listed in a Ministry of Power Rajya Sabha reply as having a policy. I have not seen it.**



**\*\*Cross-state patterns\*\***

**- Re 1 per unit support is common, with different durations.**

**- A 51% renewable condition applies in Gujarat and Maharashtra, while UP only encourages it.**

**- Small caps (Rs 20 to 25 crore) are roughly 0.03 to 0.04% of a 1 GW project's cost of Rs 70,000 crore to Rs 1 lakh crore (my arithmetic), so large projects run through discretionary packages.**

**- Policy windows lapse or change retrospectively.**

**- Oversight is thin: no data-centre category in the environmental clearance rules, no mandatory energy or water reporting.**



**\*\*Why these sites\*\* (from the 22 reviewed)**

**Six reasons:**

**1. Existing cluster and cable connectivity (four Navi Mumbai rows).**

**2. Anchor tenant or own demand (Google at Vizag, Meta at Jamnagar).**

**3. State deals.**

**4. Owned land, power and desalinated water (Jamnagar).**

**5. New coastal cable gateway and AI-scale land (Vizag).**

**6. Talent and ecosystem (Hyderabad).**



**The 22 rows break down as follows. Tracker-only or single-source rows: Reliance Jio, Jamnagar Phase 1 and the 3 GW plan, the AWS rows, AirTrunk and the PDG 1 GW target.**



**| State | Rows |**

**|---|---|**

**| Maharashtra | 4 |**

**| Gujarat | 3 |**

**| Andhra Pradesh | 7 |**

**| Telangana | 4 |**

**| West Bengal | 1 |**

**| Multi-state | 3 |**



**\*\*Sustainability\*\***

**- \*\*Green energy:\*\* Google plans renewable generation, transmission and storage with partners, though government sources describe coal backup. Meta backs about 1 GW of RE for Jamnagar. Airtel's Nxtra reports 49% renewable power and has joined RE100. CEEW found power-sector incentives are the main lever, and developers say about 80% renewable supply is feasible.**

**- \*\*Water:\*\* no mandatory reporting and no sector-wide standard. The Down To Earth review found poor transparency at Nxtra, AdaniConneX, STT, NTT, CtrlS and Sify, and STT dropped its water figures in 2025. The Systemiq-CEEW study says water risk is underestimated. The sector used about 150 billion litres in 2024-25.**

**- \*\*Verdict:\*\* sustainability is a condition added to the deal, not the stated siting reason in any of the 22 rows.**



**ETHICAL CONSIDERATIONS SURFACED:**

**- \*\*Public and government data:\*\* the legal basis is policy documents, government orders, Parliament replies and clearance filings. The UP policy was read directly from the state's site, and the West Bengal notification cover was read directly. Telangana primary text could not be obtained.**

**- \*\*Aggregated and tracker data:\*\* capacity relies partly on Wikipedia, trackers and trade sites (aidatacenterindex, Blackridge, Baxtel, DCD-type sources). The dataset is explicitly "not a census", many rows have a single source, and the `verification` column grades the evidence.**

**- \*\*Secondary-source reliance:\*\* most policy detail came from press and law-firm summaries. I flagged this repeatedly, called weak sources weak (a Google Doc export, exam-prep sites), and labelled the West Bengal body text as coming from a mirror.**

**- \*\*Privacy and consent in the research workflow:\*\* the data is organisational and policy-level. The only personal information handled was the user's own: I withheld the roll number from the proposed memory file, and I did not store anything without the user's confirmation. Quoted officials are public statements.**

**- \*\*Social and environmental impact:\*\***

&#x20; **- \*\*Vizag:\*\* a PIL alleging clearance irregularity (0.86 km from a wildlife sanctuary, Category A versus B2 dispute), 160 acres of temple land, reported National Green Tribunal cases, and citizen concern about reservoir supply and city water shortage.**

&#x20; **- \*\*Wider water stress:\*\* Visakhapatnam has the state's lowest groundwater availability, and AP is planning an inter-basin transfer for data centres.**

&#x20; **- \*\*Regulation:\*\* environmental clearance does not assess operating power or water.**

&#x20; **- \*\*Scrutiny:\*\* Indian authorities are reportedly questioning Amazon's water use.**

**- \*\*Use of AI-assisted tools and error handling:\*\* web search and fetch results were treated as leads and checked against primary text where possible.**

&#x20; **- \*\*Corrections made in the chat:\*\***

&#x20;   **- The `year\\\\\\\_note` claim in the README was wrong and was fixed.**

&#x20;   **- The UP target conflict (2 GW versus 20,000 MW) was resolved by the primary text.**

&#x20;   **- "No AP renewable share" was corrected by the 25 September statement.**

&#x20;   **- UP and West Bengal "not found" cells were filled.**

&#x20;   **- Chhattisgarh was corrected.**

&#x20; **- \*\*Tagging:\*\* rationale bullets were tagged \[S]/\[I] to separate sourced facts from inference.**

&#x20; **- \*\*Verification:\*\* the sum snippet was run, and "verify before citing" lists were provided.**

&#x20; **- \*\*Failures:\*\* one fetch failed and another source was used. Telangana primary text was never retrieved.**

**- \*\*Transparency about uncertainty:\*\***

&#x20; **- \*\*Conflicting figures:\*\* Gujarat's installed capacity (69 versus about 74 GW), UP's target, Yotta's scalability (1 GW versus 2 GW), Reliance's Visakhapatnam versus Vizianagaram location, and the Meta/Sify rumour.**

&#x20; **- \*\*Unconfirmed claims:\*\* the Google coal-backup report, zero-water cooling claims, the 70% AP rule, and the electricity-duty exemption on the Maharashtra and Telangana summaries.**

&#x20; **- \*\*Data caveats:\*\* most rows are announced or planned rather than operating, so location reasons are partly inferred.**

**- \*\*Conflicts of interest and source bias:\*\* many sources have an interest in the outcome (company press releases from Reliance, Google and Meta, state government announcements of incentives, trade trackers, ministerial statements). I tried to balance them with petitioner and critic positions (the Human Rights Forum, Green Visakha) and kept political commentary neutral.**

**- \*\*Methodological safeguards already in place:\*\***

&#x20; **- \*\*Dataset:\*\* the `sum\\\\\\\_ok` flag, the 11 `excluded` rows kept for audit, the `verification` and `source` fields, and the "do not sum" notes for nested rows.**

&#x20; **- \*\*Policy work:\*\* preference for primary documents, an explicit "verify" list, and cells marked "not found" rather than guessed.**



**WHAT TO IGNORE:**

**- Earlier statements now superseded:**

&#x20; **- UP's 20,000 MW target.**

&#x20; **- "AP has no codified renewable share" (replaced by the unverified 70% statement).**

&#x20; **- West Bengal and UP "not found" power cells.**

&#x20; **- "Nothing found" for Chhattisgarh.**

**- Repeated explanations of cables, anchor tenants and the incentive tables.**

**- The failed fetch of the Cyril Amarchand blog.**

**- The rationale column's tab-separated formatting instructions.**

**- The unconfirmed memory-import plan, unless the user returns to it.**



##### **Context from m2023bsass013@stud.tiss.edu | DISSERTATION**



**# Chat Brief: Data, Literature and Verification Workstream (compiled 19 Nov 2026)**



**\*One of several chats that make up Chetan's dissertation project. Self-contained. It supersedes `dissertation\_context\_brief\_v2.md` (dated 28 Sept 2026), which is out of date on Parliament figures and later steps.\***



**---**



**## TASK**



**Chetan (B.S. Analytics and Sustainability Studies, TISS, Roll No. M2023BSASS013) is writing a dissertation: \*"Assessing the Environmental and Grid Sustainability of India's AI Data Center Expansion: A Policy and Quantitative Energy Modeling Analysis."\* Focus (confirmed): can India's renewable energy (RE) meet the electricity demand created by AI data center expansion, and do regulatory and procurement mechanisms exist to make that happen? Water/cooling is a secondary cross-check.**



**\*\*This chat built the evidence base:\*\* data-source mapping, a Lens.org bibliometric gap analysis, a four-component analysis structure, scrapers and their verification, verification of official Parliament figures, and a cleanup plan for the facility dataset. Workflow: Claude researches and writes prompts/reports/CSVs; Chetan runs prompts in an external coding agent (Windows, Python 3.11) and pastes output back; Claude reviews it.**



**\*\*Upcoming use of these briefs:\*\* a Research Ethics assignment (identify ethical issues, explain the reasoning, describe safeguards). The ethics section below is grounded only in things that happened in this chat.**



**---**



**## CURRENT STATE**



**### A. Framing**

**- \*\*Problem statement:\*\* AI data centers create a new, dense, unusually steady category of electricity demand that is outpacing planning; unclear whether RE at current/projected buildout can meet it where and when it arises, or whether regulatory/procurement mechanisms can make that happen. The dissertation sizes the demand, tests it against India's RE potential, and evaluates the policy gaps.**

**- \*\*Four components, to be analysed one at a time\*\* (variable lists, availability scores and reading lists exist; the analyses have not started):**

&#x20; **1. \*\*Demand side:\*\* facility location/count/capacity (\~55-65% available), workload type AI vs general (\~30%), power density (\~20%, global benchmarks only), load profile (\~15%), power source (\~25%). Plan: top-down from official projections plus bottom-up for a few named mega-projects.**

&#x20; **2. \*\*Supply side:\*\* installed RE by state (\~95%), site solar/wind resource (\~95%), seasonal variation (\~70%), storage costs/plans (\~75-85%), transmission headroom near clusters (\~15-20%, likely a stated limitation).**

&#x20; **3. \*\*Regulatory layer\*\* (qualitative): Green Open Access Rules 2022 and RPO targets (\~90%), RPO compliance by state (\~75%), PPA tariffs (\~60%), inter-state banking rules (\~30%), clearance records (\~40%), disclosure mandates (\~5-10%, essentially none).**

&#x20; **4. \*\*Water/cooling:\*\* cooling type per facility (\~5%), WUE (global benchmarks only), national aggregate (\~30%), geographic overlay with water stress (\~70%).**

**- \*\*Data-availability pattern (a finding in itself):\*\* supply-side and policy data are strong (85-100%); facility-level demand-side data is weak (5-30%).**

**- \*\*Concepts explained to Chetan:\*\* data center types (enterprise, colocation, hyperscale, cloud, edge), Uptime Tier I-IV, workload classes (general about 4-10 kW/rack; AI/HPC about 40-230+ kW/rack), PUE, WUE, rack/U, redundancy. The per-component rack power percentages Claude gave were \*\*approximations and unsourced\*\*.**



**### B. Bibliometric gap analysis (Lens.org)**

**- Six Scholarly Search queries (manual CSV export), designed as a comparison matrix: \*\*A\*\* DC AND AI AND India AND energy (core gap); \*\*B\*\* DC AND AI AND energy, no India; \*\*C\*\* DC AND India AND energy, no AI; \*\*D\*\* AI AND macro grid/electricity demand; \*\*E\*\* RE AND India AND industrial demand-matching; \*\*F\*\* DC AND India AND water/cooling.**

**- \*\*Latest counts:\*\* A=27, B=1,000 (export cap; true total higher), C=71, D=10,750, E=103, F=29. Overlap: A shares 22 records with C, 6 with B, 10 with D. Older counts (A=33, B=50,000, C=109, E=202, F=141) came from buggy queries and are obsolete.**

**- \*\*Findings (from an earlier notebook run; re-verify against the latest):\*\* the target region is nearly empty (about 0.35% of the combined corpus); only about 5.3% of keyword-network edges bridged AI and power clusters, and those used AI as a forecasting tool, not as the subject of demand; only 3-5% of India-restricted results came from India-based publishers. Honest framing: adjacent literature exists (global AI-DC methods, India RE-industrial matching) but almost nothing at the exact intersection, and Lens covers scholarly output only.**

**- \*\*Notebook:\*\* per-query profiles, comparative analysis, bubble/quadrant charts, white-space density map, keyword network, NMF topics, growth curves, radar, scorecard and verdict. A reusable, topic-agnostic \*\*skill\*\* (`bibliometric-gap-analysis.skill`) was packaged. A \~1,000-word report exists but uses the obsolete counts.**

**- \*\*Not yet done:\*\* the \*\*3000-word report\*\* from the latest notebook (simple language, image placement marked), and the skill update that adds a post-export relevance filter.**



**### C. Verified/curated data work**

**- \*\*Files in `/mnt/user-data/outputs/`:\*\* source list (28 sources), GitHub repos (11), variable-to-source map, 20-variable availability table, news CSV (13 articles, window Mar-Sep 2026, needs refreshing for Oct-Nov), statewise DC CSV, DC-state-vs-RE-procurement CSV, global impact assessment report, reading lists, and agent prompts (scraper, verification, Parliament, facilities cleanup).**

**- \*\*State alignment:\*\* Maharashtra, Tamil Nadu, Karnataka = large DC hubs with strong RE and RPO compliance. \*\*Telangana and West Bengal = large AI DC pipelines but poor RPO compliance/data\*\* (strongest evidence for Objective 2). \*\*Gujarat (53,634.74 MW) and Rajasthan (50,718.39 MW)\*\* lead RE capacity (Aug 2026) with almost no DCs; siting there is an \*\*untested hypothesis\*\* (water cross-check pending). Exact RE MW for Telangana, UP, West Bengal, Haryana, Bihar, Odisha, AP not yet pulled.**

**- \*\*Google-Adani Vizag case:\*\* about 1 GW target on 601.4 acres, three SPVs; land allotted by an AP government order (Oct 2025) and more support in April 2026; ECs issued 18 Apr 2026, appraised as Category B (state level); about 90% of one site reportedly inside Pedda Chukka Konda Reserve Forest; activists allege rushed clearance; Andhra HC (Aug 2026) told the state to ensure all clearances; a PIL followed in mid-Sept; Reuters reported protests over water and wildlife; Land Conflict Watch documents land-acquisition disputes involving Dalit farmers; Visakhapatnam groundwater reported at 2.12 TMC (Apr 2026); seawater cooling proposed but ratio unclear.**

**- \*\*Other facts:\*\* WRI India: 75% of DCs in 5 states, many water-stressed. IEEFA: 262 DCs, 1.4 GW to about 9 GW by 2030. CEEW: DCs about 0.5% of national electricity and about 150 billion litres of water in 2025, both doubling by 2030. Down To Earth: no state policy requires water disclosure. IEA (Apr 2026): about 485 TWh in 2025, about 950 TWh by 2030.**

**- \*\*Reading lists per component\*\* (Xiao et al. 2025 \*Nature Sustainability\*; LBNL 2024; IEA 2025/2026; Google 24/7 CFE methodology; WRI Aqueduct; Mytton 2021; Nature Reviews Clean Technology 2025; IEEFA GEOA assessments).**



**### D. Scrapers and verification (agent-run)**

**- Four scrapers built and run: `facilities.csv` (37 rows), `news\_log.csv` (920 articles), CEA emission-factor checker, official-projections monitor (351 rows), plus `benchmark\_assumptions.csv`.**

**- \*\*CEA CO2 Baseline Database V22.0 (Aug 2026), FY2025-26, all-India weighted average incl. RES and captive:\*\* \*\*0.6780 tCO2/MWh excluding imports\*\* (Results!O14); 0.6751 including imports (AA14). Build Margin 0.4459; Combined Margin 0.7077 excl. / 0.7047 incl. FY2024-25 revised to 0.7121 excl.; V21.0 had 0.7117. The agent recommended the incl.-imports figure, which is the wrong variant for continuity. Only a single all-India factor exists (no regional factors). \*\*Values come from the agent's extraction and have not been checked against the workbook\*\* (cells O14, O16, O17).**

**- \*\*Reliance Jamnagar:\*\* 168 MW (Meta anchor-tenant AI facility, per a tracker quoting a 10 June 2026 Reliance release) is \*\*nested inside\*\* a 1 GW Phase 1 and a 3 GW master plan; never sum them. Primary Reliance release not yet obtained.**

**- \*\*Projections log triage:\*\* A (data-center-specific) 9, B (demand-forecast documents) 50, C (marginal) 238, D (irrelevant) 54. Baseline of about 375 MW (2020) to about 1,500 MW (2025) comes from the March 2026 reply.**



**### E. Parliament figures (three, different scopes; not a "doubling")**

**- \*\*13.56 GW\*\* for 2031-32, \*\*data centres in general\*\* (incl. AI): Rajya Sabha written reply, \*\*13 Mar 2026\*\*, MoS Electronics and IT Jitin Prasada citing the Ministry of Power. Same reply: 38,231 GPUs via 14 empanelled providers at about Rs 65/GPU-hour.**

**- \*\*26.3 GW\*\* additional load from \*\*AI data centres\*\* by 2031-32, "primarily served by renewable energy": Rajya Sabha written reply, \*\*27 Jul 2026\*\*, MoS Power Shripad Naik. Same reply: non-fossil share 54.2%; RE incl. large hydro +116,487 MW vs thermal coal +21,080 MW (FY2023-24 to June 2026); NEP transmission about Rs 9,16,142 crore.**

**- \*\*About 17 GW\*\* for data centres up to 2031-32 "as per CEA": Rajya Sabha reply reportedly \*\*7 Aug 2026\*\*, Prasada (date/wording from press; verify). Capacity reported about 1,575 MW.**

**- \*\*All three confirmed by multiple press reports only; Claude has not seen the Parliament documents.\*\* A PIB release (PRID 2239616, cited by a blog) reportedly covers the March reply. The meaning of "load" (peak/connected/IT/total) is unconfirmed.**

**- \*\*The agent's "primary" Parliament output was not trustworthy:\*\* its log shows no document fetch; it gave "Unstarred Question No. 956 / No. 2468", MP names and "Session 263/264" (a document labelling the first part of the 2026 Budget Session as the 270th session contradicts this); a "17.0 GW grid applications + 9.3 GW pipeline" split that sums exactly to 26.3 and looks invented (17 GW is actually the CEA figure above); a "connected/peak" definition and "Midterm Review of the 20th EPS" basis that nothing supports; and a generic URL, not a document link. Treat these as \*\*unverified\*\* until seen on sansad.in or PIB.**

**- Claude corrected the impact assessment, availability table and v2 brief to say "three figures, different scopes".**



**### F. Facilities dataset cleanup (prompt written, not yet run)**

**- `facilities.csv`: 37 rows, about 4,850 MW claimed, about 1,500 MW doubtful. A \*\*third-party review (unverified)\*\* flagged: AWS ap-south-1 tagged Hyderabad; Google Mumbai/Delhi regions tagged Vizag and overlapping the 1,000 MW hub; NTT/Neysa "Telangana" tagged Greater Noida; AIRAWAT (600 MW, likely a C-DAC supercomputer in Pune); city-market totals mixed with facility rows (Yotta Mumbai 289, CtrlS Mumbai 57, CtrlS Hyderabad 38, Nxtra Pune 32, NTT Bengaluru 162, NTT Kolkata 67); duplicate Nxtra/Airtel Kolkata; stale Wikipedia figures; blanket "AI / GPU Compute" labels; broken ₹ encoding; Kolkata over-represented (about 20 rows); Chennai, Navi Mumbai, Bengaluru, Pune thin.**

**- `facilities\_cleanup\_agent\_prompt.md` requires the agent to verify every review point itself, split into facility / city-market / cluster tables, use claimed vs verified capacity columns, tier sources (1 official, 2 reputable press/market research, 3 trackers/Wikipedia), require tier 1-2 corroboration for rows of 100 MW or more, use a controlled AI-workload vocabulary (default "unknown"), fix encoding, and log every change. Candidate clusters: Mumbai/Navi Mumbai, Pune, Chennai, Hyderabad, Bengaluru, Delhi NCR, Kolkata, Visakhapatnam, Jamnagar.**



**### G. Open decisions and pending work**

**- \*\*Decisions:\*\* Component 1 bottom-up scope (named mega-projects only or also general DCs); Component 2 hourly vs monthly matching; Component 3 diagnostic-only or with recommendations; Component 4 groundwater (CGWB) pull for Gujarat/Rajasthan; add relevance filter to the skill.**

**- \*\*Pending:\*\* 3000-word bibliometric report; run the facilities cleanup; retrieve the Parliament documents; verify the CEA cells; get the Reliance primary release; MNRE state-wise MW for six states; refresh news for Oct-Nov 2026 and check Vizag litigation status.**

**- Chetan's recent concerns (from his notes): unsure about the demand side, states already have general renewable-share rules but no data-center-specific rules found, water/cooling data missing, wants to tighten the problem.**



**---**



**## KEY CONTEXT**



**- \*\*Preferences:\*\* one step at a time with confirmation before big builds; explain why fixes work; plain language for setup, full technical depth for code; copyable/exportable formats (CSV, MD); when two files share a name, state download name and exact destination path; cost-conscious; \*\*wants shorter, more concise responses\*\*.**

**- \*\*Standing rules:\*\* never fabricate (write "Not disclosed", state the gap); every number in a written interpretation must be printed by code just above it; cite CEA version and variant; flag round-number export caps wherever the count is used; separate primary from secondary sources; quote at most 25 words.**

**- \*\*Key figures:\*\* emission factor 0.6780 (V22.0); demand 13.56 / about 17 / 26.3 GW (different scopes); storage target 236 GWh by 2031-32; Uptime rack densities (about 11 kW modal, AI up to about 142 kW).**

**- \*\*Sources reused:\*\* CEA, MNRE, rpo.gov.in, NIWE/Global Solar Atlas, IMD (some data chargeable), PARIVESH, PIB, Rajya Sabha/Lok Sabha sites, CEEW, WRI India, IEEFA, JLL, aidatacenterindex.com, DataCenterMap, Wikipedia, Lens.org.**



**---**



**## ETHICAL CONSIDERATIONS SURFACED**



**\*\*Data sourcing and consent\*\***

**- All data are public, government, institutional or commercial web sources. No participants, surveys or interviews, and no personal data were collected, so no consent process arose.**

**- \*\*Scraping:\*\* DataCenterMap, aidatacenterindex.com, Wikipedia, Google News RSS, PIB and CEA pages were scraped. Safeguards written into the prompts: check robots.txt, wait 2.5-3 s between requests, use an academic User-Agent, never bypass logins or paywalls. The paid Arizton report was deliberately not scraped. DataCenterMap rate-limited the scraper (HTTP 429) and the pipeline degraded gracefully.**

**- \*\*Deviations found in the agent log:\*\* exploratory probes used a Chrome-style User-Agent, browser-like headers and Playwright on DataCenterMap, against the "identify as academic research" rule; the academic User-Agent carried a \*\*placeholder contact address\*\* that is not the researcher's own; no terms-of-service review was recorded.**

**- \*\*Crowd-sourced/aggregated data\*\* (Wikipedia lists, DataCenterMap, aidatacenterindex.com, whose rows contradicted their own names) are treated as leads, not evidence, with tier 1-2 corroboration required for large rows.**

**- \*\*Public records\*\* (Parliament replies, CEA workbook, MNRE, PIB, rpo.gov.in) are used but the actual Parliament documents have not yet been retrieved and cited. Some IMD data may be chargeable.**

**- \*\*Copyright:\*\* quotations capped at 25 words; no paywalled content reproduced.**



**\*\*Privacy and confidentiality\*\***

**- Only facility, operator and policy data were handled. Named individuals appear only as public officials in Parliament records (the agent's unverified MP names should not be cited). The Land Conflict Watch case about Dalit farmers' land is used as context only, with no personal identifiers collected.**

**- Modelling at cluster level reduces reliance on site-level detail about critical infrastructure.**



**\*\*Social and environmental impact\*\***

**- Vizag: reported forest-reserve overlap, wildlife concerns, rushed Category B clearance allegations, land-acquisition disputes, protests, and court challenges (Andhra HC, PIL). The researcher relies on news and court reporting for these, not on primary documents.**

**- DCs are concentrated in water-stressed states; groundwater in Visakhapatnam is critically low; the seawater-cooling plan is unclear.**

**- The \*\*Gujarat/Rajasthan siting idea is unvetted\*\* for water, land-use and community effects and must be presented as a hypothesis until the groundwater cross-check is done.**

**- Excluded advocacy reposts (e.g., Countercurrents) from the news CSV for editorial quality; community-objection perspectives were kept via mainstream, court and NGO-research sources. This is a balance decision to disclose.**



**\*\*AI-assisted and automated tools: reliability and error handling\*\***

**- Claude and an external coding agent were used throughout. Errors that were caught and fixed:**

&#x20; **- Lens queries: a literal "(same)" placeholder (returned 7.4 million records), searching Patents instead of Scholarly Works, and ambiguous bare terms (e.g., "open access") that pulled in unrelated papers. The user spotted the irrelevant results.**

&#x20; **- White-space score contaminated by generic energy terms, and a written "<0.05%" that contradicted the printed \~1.9%.**

&#x20; **- The agent chose the wrong emission-factor variant and invented a reason the 26 GW source was missing (it was a parliamentary reply).**

&#x20; **- The agent's Parliament output claimed primary citations without any logged document fetch, with unsupported details.**

&#x20; **- Scraper output with wrong cities, duplicates, mixed scopes and over-labelled "AI" rows.**

**- \*\*Claude's own errors:\*\* asked for regional emission factors that do not exist; stale counts in the first 1,000-word report; unsourced rack-power percentages; "nearly doubled" framing; cited a secondary source for the demand figure.**

**- \*\*Safeguards:\*\* independent re-checking of agent output; no-fabrication rule; print-then-cite for every number; fetch logs and changelogs; claimed vs verified columns; a packaged skill that encodes the lessons.**

**- \*\*Limits:\*\* Claude cannot open Chetan's local files and relies on pasted output; CEA workbook values remain unchecked.**



**\*\*Transparency about limitations and unverifiable claims\*\***

**- No complete official facility census exists; trackers disagree (Karnataka 5 vs 26 facilities). Per-facility AI classification, power density, load profile, cooling type, water use and transmission headroom are not publicly disclosed, so global benchmarks and stated assumptions are used.**

**- Lens covers scholarly output only; Query B is export-capped; the three demand figures have different scopes and an unconfirmed load definition; keyword scoring has false positives and an arbitrary 0.6 threshold; "verified" labels mean a source was found, not that the operator's primary release was seen.**



**\*\*Potential conflicts of interest\*\***

**- Sources with commercial or promotional interests: operator press releases (Reliance, Google, Adani), investment-promotion pages (Invest India), paid market research (Arizton), hyperscaler self-reports (Microsoft), and an unclear-provenance tracker.**

**- The Google 24/7 CFE methodology paper is proposed as core method while Google is a party to the Vizag project.**

**- Paywalled data (Arizton, about $5,000) was not used, so the study leans on free sources, a possible selection bias.**

**- No researcher conflict of interest was raised in this chat.**



**\*\*Accuracy and integrity safeguards in the methodology\*\***

**- Source tiering and provenance columns; primary vs secondary labelling; export-cap flagging; non-overlapping scoring vocabularies; relevance filter; empty results shown as findings; CEA version and variant stated; reconciliation tables; programmatic percentages.**



**\*\*Not yet addressed (candidates to check, not issues encountered):\*\* a terms-of-service and licence review for scraped sites; a real contact address in the User-Agent; a statement on AI-tool use as required by TISS policy; a conflict-of-interest declaration by the researcher.**



**---**



**## WHAT TO IGNORE**



**- `dissertation\_context\_brief.md` (v1) and `dissertation\_context\_brief\_v2.md` (superseded by this file); the five older bibliometric prompt files.**

**- Old query counts (A=33, B=50,000, C=109, E=202, F=141) and the 1,000-word report built on them.**

**- 0.7117 as the current emission factor; 0.6751 as the recommended citation; regional emission factors.**

**- "26 GW" as a precise figure; any claim that the demand estimate "nearly doubled"; the agent's Parliament details (question numbers, MP names, session numbers, 17+9.3 GW split, "Midterm Review" basis, "connected/peak" definition).**

**- The third-party facilities review points until the cleanup run verifies them.**

**- Unsourced rack-power percentage breakdowns; the news window of Mar-Sep 2026 as "latest".**

**- Repeated explanations, verbatim agent logs and tool-call transcripts.**





##### **Context from raxscience@gmail.com | Water and energy risk scoring**



**Google Sheets is connected now, so I'll load the tools and read the headers from each tab.**



**The sheet already has a "Data Dictionary" tab, so I'll read it first, along with the header rows and a few sample rows of every other tab.**



**The "Data Dictionary" tab exists but is empty (frozen header row, 220 rows), so I'll fill that one and add no new tab. First I'm checking the Coordinates tab for the column misalignment you flagged.**



**The District Combined section is written (rows 2–49). Next are Data Centres, Groundwater and Block Categories.**



**Next are the remaining tabs: Tap Water, Power, Energy, the three Grid tabs and Coordinates.**



**Two cells need small fixes, and I'll add a legend at the bottom. Then I'll check the result.**



**I filled the empty \*\*Data Dictionary\*\* tab in your sheet with 189 variables, one row per column across the 11 data tabs. I checked it against the live headers: every column in District Combined, Data Centres, Groundwater, Block Categories, Tap Water, Power Hours, Energy Inputs, Grid (all three) and Coordinates appears once, in tab order. I didn't touch any other tab and didn't redo any calculations.**



**Each row has the tab, variable name, plain-language meaning, unit, data type, source, role in scoring, caveats and a confidence marker. The last rows hold a key for source tiers, units (ham, MU, IT vs facility MW, WUE) and a one-line scoring flow.**



**- \*\*Confidence:\*\* 14 descriptions are marked "Inferred – confirm" because I worked them out from the column name alone, such as `type` in Grid - Evidence and the empty coordinate columns in Data Centres. Please check those.**

**- \*\*Spot checks:\*\* I recomputed a few values from the sample rows. `stage\_of\_extraction\_pct`, `W\_equity`, `E\_baseline`, `DC\_demand\_pressure\_pct`, `E\_combined` and `Overall\_Risk` all matched the sheet.**



**\*\*Things worth knowing from the read:\*\***

**1. \*\*W\_combined:\*\* In the sheet it equals W\_baseline, with data centre water demand excluded from scoring. Your earlier design re-ran the CGWB bands with that demand added. The dictionary describes what the sheet does, so update your methodology doc to match.**

**2. \*\*DC\_demand\_pressure\_pct:\*\* It adds planned IT-load MW and planned facility-load MW together, although the sheet keeps those two bases separate elsewhere. The denominator is state peak demand, not district.**

**3. \*\*Coordinates tab:\*\* The columns are aligned. The first 21 rows hold the source tier inside `status`, and the newer rows use the `source\_tier` column. The Data Centres latitude and longitude columns are still empty in the rows I read.**

**4. \*\*Red Card override:\*\* I couldn't confirm that the override for MSEDCL, TNPDCL, BESCOM and UHBVNL was applied to `DISCOM\_score\_clean`. The dictionary asks you to check.**

**5. \*\*README:\*\* It still says 22 of 118 coordinates; the Coordinates tab now has 43.**

**6. \*\*Number format:\*\* `planned\_ultimate\_mw` and the Energy Inputs peak demand columns are stored as text with commas, so convert them before doing sums.**







