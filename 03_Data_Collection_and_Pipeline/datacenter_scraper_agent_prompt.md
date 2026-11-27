# Prompt: Build a Multi-Source Python Scraper for India Data Center Demand-Side Data

## Context

I am building the "Demand Side" component of a dissertation on AI data center energy demand in India. I need a Python-based scraping system that pulls together data center facility information (location, capacity, operator, workload type where available) and monitors for new announcements and official demand-projection reports. This is NOT a single scraper — it's a small collection of purpose-built scripts, each targeting a different source, because no single site has all the data.

## Important ground rules before writing any code

1. **Respect `robots.txt` and rate-limit every request.** Check each target site's `robots.txt` before scraping it. Add a minimum 2–3 second delay between requests to the same domain. Set a descriptive `User-Agent` header identifying this as academic research, not a bot pretending to be a browser.
2. **Prefer structured data over raw HTML scraping wherever possible.** If a site offers an API, RSS feed, or a downloadable CSV/XLS, use that instead of parsing HTML — it's more stable and less likely to break when the site's design changes.
3. **Do not scrape sites that require login/paywall bypass** (e.g., do not attempt to scrape Arizton's paid report — that data is intentionally behind a paywall and scraping around it is out of scope).
4. **Every scraper must degrade gracefully.** If a page structure has changed and a scraper can't find expected elements, it should log a clear warning and skip that source, not crash the whole pipeline.
5. **Every scraped record must carry its source and retrieval date**, so downstream analysis in the dissertation can cite exactly where and when each data point came from.

## Scraper 1: Data Center Facility Directory (location, operator, status)

**Target sources (in priority order):**
- `datacentermap.com/india/` — facility name, city, operator
- Wikipedia pages: `Data centre industry in India`, `List of data centres in West Bengal` (and check if similar structured lists exist for other states — search Wikipedia for "List of data centres in [state]" for each major DC state: Maharashtra, Tamil Nadu, Karnataka, Telangana, Uttar Pradesh)
- `aidatacenterindex.com` — for facilities it explicitly tags as AI-specific, including capacity and status where shown

**Implementation notes:**
- For Wikipedia, use `pandas.read_html()` on the page URL first — many of these lists are already in clean `<table>` elements, which pandas can parse directly without manual HTML parsing.
- For DataCenterMap.com and AI Data Center Index, inspect the page structure first (view page source or use browser dev tools) before writing a parser — these are likely to use JavaScript-rendered content, in which case `requests` + `BeautifulSoup` won't see the data and you'll need `playwright` or `selenium` instead. Check for a "view-source" static HTML version first, since headless browsers are slower and more fragile.
- Deduplicate facilities across sources by matching on (operator name + city), since the same facility will likely appear on multiple sites with slightly different naming.

**Output schema (`facilities.csv`):**
```
facility_name, operator, state, city, capacity_mw, capacity_source_note, workload_type, status, source_url, source_name, date_scraped
```
Where a field isn't available from any source, write `"Not disclosed"` — never leave it blank or guess a value.

## Scraper 2: News & Announcement Monitor (commissioning timelines, new projects)

**Purpose:** Since commissioning timelines and new project announcements aren't in any structured database, this scraper monitors news sources on an ongoing basis rather than doing a one-time pull.

**Approach:**
- Use Google News RSS feeds (no API key needed): `https://news.google.com/rss/search?q=<query>&hl=en-IN&gl=IN&ceid=IN:en`
- Run this with multiple queries: `"data center" India AI`, `"data centre" India investment`, `hyperscale India MW`, and any specific named projects you're tracking (e.g., `"Google Adani" data center`, `"Reliance Jamnagar" AI`)
- Parse each RSS feed's items: title, link, publication date, source
- Store results in a running log (`news_log.csv`), appending new entries each run rather than overwriting, and deduplicating by article URL
- This becomes your evidence base for commissioning timelines — a human (me) will still need to read the flagged articles and manually extract the actual "goes live in [year]" detail, since that phrasing varies too much to reliably auto-extract, but the scraper's job is to surface the relevant articles so I don't have to manually search every week.

**Output schema (`news_log.csv`):**
```
headline, source, publication_date, url, query_matched, date_scraped
```

## Scraper 3: CEA Grid Emission Factor Checker

**Purpose:** This is the one variable in the whole set with a single authoritative, versioned official source. The scraper's job is simply to check whether a newer version has been published, and download it if so.

**Target:** `cea.nic.in/cdm-co2-baseline-database` (or wherever CEA currently hosts the CO2 Baseline Database page — verify the current URL, as government site structures change)

**Approach:**
- Scrape the page for the current listed version number (e.g., "V21.0") and publication date
- Compare against the last-known version stored locally (`last_known_version.txt`)
- If a new version is found, download the linked PDF/XLS file and log the new emission factor value + version + date
- This should run on a schedule (e.g., monthly) rather than constantly, since CEA updates this infrequently

## Scraper 4: Official Demand Projection Monitor

**Purpose:** Track when CEA, Ministry of Power, or PIB publish new data-center-specific demand projections (like the 26 GW by FY2031-32 figure), since these appear irregularly in press releases and reports rather than a structured feed.

**Approach:**
- Monitor PIB's press release RSS/search (`pib.gov.in`) for the Ministry of Power, filtered by keywords: "data centre", "data center", "AI", "electricity demand"
- Monitor CEA's reports page (`cea.nic.in/reports`) for new National Electricity Plan or Resource Adequacy Plan document uploads
- Log any new matching document found, with title, date, and link, into `official_projections_log.csv` — again, a human will need to actually read and extract the specific figures, since these are unstructured PDF reports, not tables

## What NOT to build (explicitly out of scope)

- **Do not attempt to scrape or infer power density (kW/rack) values.** This is not published anywhere as a live, updatable data source — it comes from a periodic Uptime Institute survey PDF. Instead, create a small static reference file `benchmark_assumptions.csv` with the known published figures (e.g., "General-purpose rack: ~8-10 kW", "AI/HPC rack: ~100-230+ kW, source: Uptime Institute Global Data Center Survey") that gets manually updated once a year when a new survey is published, not scraped.
- **Do not attempt to scrape or infer load profile or current-power-source data.** Same reasoning — these exist only as qualitative commentary in reports (IEA, CEEW), not structured data. Store these as documented assumptions with citations in the same `benchmark_assumptions.csv` file, not as scraper output.
- **Do not scrape Arizton or any other paywalled market report.**

## Technical Requirements

- Python 3.10+, using `requests`, `beautifulsoup4`, `pandas`, `feedparser` (for RSS), and `playwright` only if a target site requires JS rendering (check this first before assuming you need it)
- Each scraper should be its own standalone script (`scraper_facilities.py`, `scraper_news.py`, `scraper_cea_emission_factor.py`, `scraper_official_projections.py`), plus one `run_all.py` that runs them in sequence with appropriate delays between different scrapers
- All outputs go to a single `/data/` folder, with each script appending to its own CSV (not overwriting) so historical runs build up an evidence trail over time
- Add a `requirements.txt`
- Add basic logging (Python's built-in `logging` module) so each run produces a clear record of what succeeded, what was skipped, and why

## Deliverable

The four scraper scripts, the `run_all.py` orchestrator, the `benchmark_assumptions.csv` static reference file (pre-populated with the known Uptime Institute and IEA figures I've already sourced), a `requirements.txt`, and a short `README.md` explaining how to run each script and what each output file contains.
