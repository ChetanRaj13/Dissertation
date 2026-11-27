# Dissertation Project — Full Context Brief

## TASK

Chetan (B.S. Analytics and Sustainability Studies, TISS, Roll No. M2023BSASS013) is writing a dissertation, working title:
**"Assessing the Environmental and Grid Sustainability of India's AI Data Center Expansion: A Policy and Quantitative Energy Modeling Analysis"**

**Core pivoted focus (confirmed direction):** India's renewable energy (RE) potential to meet the electricity demand created by AI-driven data center expansion — i.e., can India's solar/wind/storage capacity actually match the load AI data centers are adding to the grid, and what regulatory/policy mechanisms exist (or don't) to make that happen.

Original broader proposal covered grid + water + policy + AI efficiency modeling with three objectives: (1) model regional electricity demand/emissions/water use under efficiency scenarios, (2) evaluate regulatory weaknesses around RE integration/PPAs/resource conservation, (3) develop evidence-based regulatory mechanisms. The RE-focus pivot narrows Objective 1 toward RE-supply-gap analysis and Objective 2 toward RE-specific regulatory levers (PPAs, open access, RPOs).

## CURRENT STATE / WHAT'S BEEN DONE

### 1. Data source mapping (three rounds)
- Compiled ~28 web/policy/think-tank sources (CEEW, CEA, MNRE, NIWE, Global Solar Atlas, Green Open Access Rules 2022, IEEFA, etc.) as a CSV with relevance ratings.
- Compiled ~11 GitHub repos (grid-india scrapers, RenewableEnergy_India_Dataset, PyPSA, data-center location trackers) as a second CSV.
- Later built a **master "Variable → Data Availability" CSV** covering 20 modeling variables (DC location, DC type, capacity, power density, load profile, cooling tech, water use, solar/wind resource, installed RE capacity, transmission headroom, storage cost, seasonal variability, ambient temp, RE procurement policy, grid emission factor, RPO compliance, state DC distribution, regulatory clearance status, literature coverage) each with: real source link, and a **% data availability score with justification**.
  - **Key finding from this table:** supply-side/policy data is strong (85–100%: grid emission factor [0.7117 tCO2/MWh, CEA, FY2024-25], RE procurement policy, installed RE capacity, battery storage, solar/wind GIS resource). Facility-level demand-side data is weak (5–30%: cooling tech, load profile, power density, DC type classification, current power source) — confirmed as a genuine, citable disclosure gap (CEEW, Down To Earth both confirm no facility discloses cooling type or water use).

### 2. Data center location/statewise data
- Built a statewise CSV of named India DC facilities (with area/MW where disclosed) + state aggregate rollups, sourced from DataCenterMap.com, AI Data Center Index, Arizton, Blackridge Research, Wikipedia's West Bengal DC list. **Explicitly flagged: no complete official facility-level census exists in India; source trackers disagree on total counts (Karnataka: 5 vs 26 facilities depending on source).**
- Confirmed AI-specific (not just "general") DC projects: Google-Adani Visakhapatnam/Anakapalli complex (~1GW target, 601.4 acres, 3 SPVs — VMDCPL/VRDCPL/Adavivaram), Reliance Jamnagar (1GW→3GW target, NVIDIA partnership), Microsoft Hyderabad "India South Central" region, AWS (670MW disclosed), CtrlS Chandan Valley Hyderabad (612MW planned).
- **Google-Adani Vizag is an active, unfolding legal/regulatory case study**: AP govt allotted land via G.O. MS. No. 40 (Oct 2025); ECs issued April 2026 (refs AP INFRA 2 EC AKP 04 2026 2516 and AP INFRA2 EC VSP 04 2026 2517); categorized as Category B (state-level, lighter scrutiny) not Category A, which activists/PIL (Andhra HC, ongoing as of Sept 2026) allege was a rushed clearance bypassing full EIA/public hearing. Land Conflict Watch also documents Dalit farmer land acquisition disputes there.

### 3. State-level RE procurement connection
- Cross-referenced DC-hosting states against RPO compliance and installed RE capacity (MNRE, rpo.gov.in, Renewable Watch, ORF).
- **Key finding:** Maharashtra/Tamil Nadu/Karnataka = strong DC hubs AND strong RPO compliance (good alignment). **Telangana and West Bengal = major/growing AI DC hubs (CtrlS 612MW, Reliance/Adani/L&T 525,000 sq ft hyperscale plots) but POOR RPO compliance (<60%) and flagged for inconsistent/unpublished data** — this is one of the strongest citable findings for Objective 2. **Gujarat and Rajasthan = #1 and #2 in installed RE capacity (53,634 MW and 50,718 MW respectively, Aug 2026) with excellent RPO compliance but almost NO current DC presence** — framed as a "strategic siting opportunity" recommendation for the dissertation's policy section.

### 4. Regulatory/official source landscape
- No single government portal lists "green-lit" data centers. Relevant fragments: PARIVESH (environmental clearance, state-level SEIAA), National Single Window System (NSWS), DPIIT sectoral FDI data, state single-window portals (Maharashtra MAITRI, Telangana TS-iPASS, AP APIIC, Tamil Nadu Guidance, UP Nivesh Mitra), PIB press releases, MeitY (draft Data Centre Policy 2020, still not finalized).

### 5. Recent news curation
- Built a CSV of ~13 high-quality news articles (last 6 months, March–Sept 2026) from credible outlets only (Reuters, The News Minute, Mongabay India, WRI India, IEEFA, S&P Global/Platts, Down To Earth, JLL, Invest India, LiveLaw). Explicitly excluded lower-quality/advocacy-blog sources.
- **Most important figures extracted:** Ministry of Power official projection of **26 GW additional load from AI data centers by FY2031-32** (S&P Global/Platts, July 2026) — the single most citable demand-side number. WRI India: **75% of India's data centers sit in just 5 states**, many in water-stressed zones. Down To Earth: **no major state DC policy requires water-consumption disclosure**. CEA is only just starting to formally direct states/DISCOMs to factor DC demand into resource adequacy plans (Outlook Business, April 2026).

### 6. Global impact assessment report (built + sourced)
- Wrote a global AI data center environmental impact report (energy/water/carbon/grid-strain/disclosure gap), each section paired directly with the matching Indian data point already established. Key global figures used:
  - IEA "Key Questions on Energy and AI" (April 2026, most current): global DC electricity ~485 TWh in 2025 (~1.5% of global electricity) → projected ~950 TWh by 2030 (~3%); AI-specific server demand tripling 2025–2030, growing ~30%/year vs ~9%/year for conventional.
  - Nature Sustainability (Xiao et al., 2025): US state-by-state AI server carbon/water footprint + net-zero pathways — **identified as the closest methodological template** for replicating a state-wise approach on India.
  - Patterns/Cell Press (2025): global AI carbon footprint 32.6–79.7 million tCO2 (2025); water footprint 312.5–764.6 billion litres (2025).
  - Nature Reviews Clean Technology (2025): "Designing and regulating clean energy data centres" — closest match to Objective 2.
  - npj Clean Water (Mytton, 2021): foundational WUE methodology paper.
  - Nature (Crawford, 2024, news feature): AI environmental costs "soaring and mostly secret" — supports disclosure-gap argument.
  - Also gave direct links to primary published reports (IEA x2, LBNL 2024 US DC Energy Usage Report, Goldman Sachs "165% increase by 2030," McKinsey "$7 trillion" capex report, Microsoft 2025 Environmental Sustainability Report as an example of the disclosure gap).

### 7. Bibliometric Gap Analysis (major workstream — most iterated part of the project)
**Method:** Six structured Lens.org Scholarly Search queries designed as a comparison matrix to find the literature gap:
- **Query A** (core intersection: AI + Data Center + India + Energy) — the target/gap query
- **Query B** (Global AI + Data Center + Energy, no India)
- **Query C** (Data Center + Energy + India, no AI — pre-AI-boom baseline)
- **Query D** (AI + macro electricity/grid demand, no "data center" term)
- **Query E** (Renewable Energy + Industrial demand-matching + India, no AI/DC — methodological precedent from other industries)
- **Query F** (Data Center + Water/Cooling + India)

**Query bugs found and fixed (important — final corrected versions):**
- Bare `"open access"` in Query E was pulling in unrelated open-access-publishing-license boilerplate (including gender studies papers) — fixed to `"green open access"` / `"renewable energy open access"`.
- Bare `grid` and `colocation` in Query A/B/C were ambiguous (grid = social theory/computing; colocation = spatial statistics) — fixed to compound phrases (`"power grid"`, `"data center colocation"`, etc.)
- Bare `water` and `cooling` in Query F were dangerously generic (hydrology, astrophysics, cryogenics) — fixed to compound phrases (`"water usage"`, `"data center cooling"`, etc.)
- **General lesson documented:** any bare single-word term with a common meaning in another academic field is high-risk; compound phrases are almost always safe.

**Final corrected result counts (after all fixes, most recent notebook run):**
| Query | Record Count | Notes |
|---|---|---|
| A (core gap) | 27 | Uncapped, complete export |
| B (global AI+DC+energy) | 1,000 | **Capped at platform ceiling — true total likely higher** |
| C (pre-AI India DC+energy) | 71 | Uncapped |
| D (AI+macro grid) | 10,750 | Uncapped — largest, most mature body |
| E (RE+industrial+India) | 103 | Uncapped |
| F (DC+water+India) | 29 | Uncapped |

Overlap matrix confirmed: Query A shares 22 records with C, only 6 with B (i.e., very few papers bridge the core Indian intersection to the global AI-DC modeling literature), 10 with D.

**Notebook structure built (via a custom-authored, packaged, reusable Claude Skill — `bibliometric-gap-analysis.skill`, validated and packaged with the skill-creator tool):**
- Section 0: setup/ingestion; Section 2 (A–F): per-query profiles (temporal trend, geography, venues, citations, keywords, word cloud, top-5-cited table, synthesis takeaway); Section 3: comparative analysis (volume bar chart, pairwise overlap matrix/heatmap, temporal overlay, keyword divergence, positioning bubble chart, thematic gap 2×2 quadrant matrix, recency-weighted growth); Section 4: advanced structural gap detection (paper-level white-space KDE density map scored on independent AI-specificity vs India/DC-specificity axes, keyword co-occurrence network graph with cross-community edge count, NMF topic modeling, cumulative growth trajectories, multi-axis radar/maturity chart); Section 5: synthesis + gap scorecard table + final bolded verdict paragraph.

**Bug found and fixed in the analysis itself (important methodological catch):** The white-space density map's `india_dc_specificity_score` word list originally included generic global energy terms ("power grid," "renewable energy," "electricity demand" etc.) alongside real India/DC terms — this caused false positives (e.g., Swiss/UK/Dutch generic energy-forecasting papers scoring as "India/DC-specific"). Also, the stated "<0.05%" target-zone figure in one draft directly contradicted the notebook's own printed count (was actually ~1.9%). **Fix applied:** stripped the word list down to only `india, indian, data center, data centre, hyperscale, colocation`; forced every percentage in the notebook to be computed and printed programmatically rather than typed by hand. After the fix, re-run showed a clean, consistent target-zone figure (**214 papers, 0.351% of the 60,952-paper combined corpus** — this was from an earlier full run; note the most recent corrected-query run above shows updated smaller totals, so this exact 214/0.351% figure may shift slightly on the latest data and should be re-verified against the current notebook state). Network graph cross-community bridging was quantified at **~5.3% (18 of 339 edges)**, and those few bridging edges were one-directional (AI used only as a forecasting tool for electricity demand, never as the subject of demand being measured) — a strong, specific, quotable structural gap finding.

**Skill file created:** A generic, topic-agnostic, file-count-agnostic version of this entire method was packaged as a reusable Claude Skill (`bibliometric-gap-analysis.skill`) — works for any number of CSVs, any topic, elicits queries/term-lists from the user rather than hardcoding AI/India, and bakes in all the bug-fix lessons (no shared vocabulary between scoring dimensions, always print-then-cite percentages, flag round-number export caps, treat empty files as findings not errors). This was successfully packaged/validated via the skill-creator tool and delivered to the user as an installable `.skill` file.

### 8. Reports written from the bibliometric notebook
- A ~1000-word simplified report (`bibliometric_analysis_report.md`) — plain language, with 5-6 marked image-insertion points referencing specific notebook chart locations (bar chart of 6 query counts, white-space density map, keyword network graph, cumulative growth chart, radar chart).
- **A 3000-word detailed version was in progress at the point of this context compaction** — user uploaded the notebook's newest/re-run state (with the corrected query results: A=27, B=1000 capped, C=71, D=10,750, E=103, F=29) and asked for a longer, still-simple report. I had extracted per-query synthesis takeaways, the volume comparison table, and the overlap matrix from this newest notebook version but had **not yet written or delivered the 3000-word report** — this is the immediate next step if resuming.

### 9. Papers found in top journals (Nature/Sustainability-tier, for lit review)
Curated 5 peer-reviewed papers: Nature Sustainability (Xiao et al. 2025 — closest methodological template), Nature Reviews Clean Technology (2025, clean energy DC regulation), npj Clean Water (Mytton 2021, WUE methodology), Nature news feature (Crawford 2024, disclosure gap), Patterns/Cell Press (2025, global carbon/water quantification). Deliberately excluded arXiv preprints since user wanted only Nature/Sustainability-tier journals (though noted these exist if wanted later).

## KEY CONTEXT (names, numbers, constraints to preserve)

- **Person:** Chetan, TISS student, Roll No. M2023BSASS013, India-based.
- **Preferences:** works one step at a time, wants explicit confirmation before proceeding on complex builds; wants explanations of *why*, not just fixes; plain language for setup/deployment steps but full technical depth for code/queries; prefers copyable/exportable formats (CSV, MD); cost-conscious/pragmatic about tooling.
- **Critical official figures to keep exact:**
  - Grid emission factor: **0.7117 tCO2/MWh** (CEA CO2 Baseline Database V21.0, FY2024-25)
  - Official demand projection: **26 GW additional load from AI data centers by FY2031-32** (Ministry of Power, via S&P Global/Platts)
  - Battery storage target: **236 GWh by 2031-32**, scaling to **890 GWh by 2036** (CEA National Electricity Plan)
  - WRI India: **75% of India's DCs in just 5 states** (Maharashtra, Tamil Nadu, Karnataka, Telangana, UP)
  - Gujarat installed RE capacity: **53,634.74 MW** (highest in India, Aug 2026); Rajasthan: **50,718.39 MW** (2nd)
- **All CSV/MD deliverables so far were saved to `/mnt/user-data/outputs/`** with filenames including: `dissertation_data_sources.csv`, `dissertation_github_repos.csv`, `lens_extract.py` / `lens_gap_analysis_extract.py`, `bibliometric_analysis_prompt.md` (superseded), `bibliometric_gap_bubble_chart_prompt.md` (superseded), `bibliometric_advanced_gap_analysis_prompt.md` (superseded), `bibliometric_bugfix_prompt.md`, `complete_bibliometric_gap_analysis_prompt.md` (superseded by the skill file), `bibliometric-gap-analysis.skill` (the final reusable deliverable), `bibliometric_analysis_report.md` (1000-word version, delivered), `data_requirements_source_mapping.csv`, `india_datacenter_news_last6months.csv`, `india_datacenters_statewise.csv`, `dc_state_vs_re_procurement.csv`, `global_ai_datacenter_impact_assessment.md`, `dissertation_variable_data_availability.csv`.
- **Standing caution the user cares about:** never fabricate precise numbers when real facility-level data doesn't exist — always mark "Not disclosed" and cite the actual gap explicitly rather than inventing plausible-looking figures. This has been a repeated, explicit expectation throughout.

## WHAT TO IGNORE

- Early versions of the six Lens.org queries (pre-bug-fix) — superseded by the corrected compound-phrase versions.
- The first "prompt" files built for the bibliometric notebook (`bibliometric_analysis_prompt.md`, the bubble-chart-only addition, the advanced-techniques addition, and even the "complete" merged prompt) — all superseded by the final generic, reusable **Skill file**, which is the only version that should be used going forward.
- The white-space density map's earlier stated "<0.05%" figure and the flawed word-list version behind it — factually wrong, already corrected.
- The very first (pre-correction) query-count numbers used in the first 1000-word report (A=33, B=50,000-capped, C=109, D=10,750, E=202, F=141) — these are from an earlier, buggier notebook run. **The most current, correct counts are A=27, B=1,000 (capped), C=71, D=10,750, E=103, F=29**, as confirmed in the latest uploaded notebook.
- Countercurrents.org and similar advocacy-blog articles surfaced during news research — deliberately excluded from the final curated news CSV for quality reasons.
