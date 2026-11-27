"""
Official Demand Projection Monitor Scraper (India)
Part of India AI Data Center Energy Demand Study

Purpose:
Monitors official government releases and planning documents from:
1. Press Information Bureau (PIB) / Ministry of Power (pib.gov.in)
2. Central Electricity Authority (CEA) Reports & Plans (cea.nic.in)
   - National Electricity Plan (NEP)
   - Electric Power Survey (EPS)
   - Integrated Resource Planning & Load Forecasting
   - Resource Adequacy Studies

Output Schema (official_projections_log.csv):
headline, publisher, publication_date, document_url, query_matched, date_scraped, notes
"""

import os
import re
import sys
import time
import logging
from datetime import datetime
from urllib.parse import quote_plus, urljoin

import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("scraper_official_projections")

USER_AGENT = "AcademicResearch-IndiaDC/1.0 (+https://github.com/dissertation-dc-india; contact: academic.dc.research@gmail.com)"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

RATE_LIMIT_DELAY = 2.5

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "official_projections_log.csv")

PROJECTION_COLUMNS = [
    "headline",
    "publisher",
    "publication_date",
    "document_url",
    "query_matched",
    "date_scraped",
    "notes",
]

GOV_RSS_QUERIES = [
    'site:pib.gov.in "Ministry of Power" "data center"',
    'site:pib.gov.in "Ministry of Power" "data centre"',
    'site:pib.gov.in "data centre" "electricity demand"',
    'site:pib.gov.in "data center" "capacity"',
    'site:pib.gov.in "Central Electricity Authority" "demand"',
    'site:pib.gov.in "National Electricity Plan"',
    'site:cea.nic.in "data centre" OR "data center"',
    'site:cea.nic.in "National Electricity Plan" OR "Electric Power Survey"',
]

CEA_MONITORED_PAGES = [
    ("https://cea.nic.in/reports/?lang=en", "CEA Reports Directory"),
    ("https://cea.nic.in/integrated-resource-planning-division/?lang=en", "CEA Integrated Resource Planning"),
    ("https://cea.nic.in/power-survey-load-forecasting-division/?lang=en", "CEA Power Survey & Load Forecasting"),
    ("https://cea.nic.in/national-electricity-plan/?lang=en", "CEA National Electricity Plan"),
]


def clean_text(text: str) -> str:
    if not text:
        return "Not disclosed"
    s = " ".join(str(text).split())
    return s if s else "Not disclosed"


def scrape_pib_government_rss(query: str) -> list[dict]:
    """Scrape official government announcements from PIB/Gov portals via RSS."""
    records = []
    encoded_query = quote_plus(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    logger.info(f"Querying Gov RSS for: '{query}'")
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(rss_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Gov RSS returned HTTP {resp.status_code} for query: {query}")
            return records

        feed = feedparser.parse(resp.content)
        entries = feed.entries
        logger.info(f"Found {len(entries)} official releases for query: '{query}'")

        for entry in entries:
            headline = clean_text(entry.get("title", ""))
            doc_url = entry.get("link", "").strip()
            pub_date = entry.get("published", entry.get("updated", today_str))

            publisher = "Press Information Bureau (PIB)"
            if "cea.nic.in" in doc_url or "CEA" in headline:
                publisher = "Central Electricity Authority (CEA)"
            elif "pib.gov.in" in doc_url or "PIB" in headline:
                publisher = "Press Information Bureau (PIB) / Ministry of Power"

            records.append({
                "headline": headline,
                "publisher": clean_text(publisher),
                "publication_date": clean_text(pub_date),
                "document_url": clean_text(doc_url),
                "query_matched": query,
                "date_scraped": today_str,
                "notes": "Official press release / announcement surfaced via government query monitor",
            })

    except Exception as e:
        logger.warning(f"Error fetching Gov RSS for query '{query}': {e}")

    return records


def scrape_cea_reports_directory(page_url: str, section_name: str) -> list[dict]:
    """
    Scrape CEA divisional and report pages for planning documents,
    NEP reports, and Resource Adequacy publications.
    """
    records = []
    logger.info(f"Scanning CEA Report page: {section_name} -> {page_url}")
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(page_url, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch CEA reports page {page_url} (HTTP {resp.status_code})")
            return records

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Search for PDF and document download links
        links = soup.find_all("a")
        for a in links:
            href = a.get("href", "")
            title_text = clean_text(a.get_text(strip=True))
            if not href or len(title_text) < 3:
                continue

            full_href = urljoin(page_url, href)
            full_href_lower = full_href.lower()
            text_lower = title_text.lower()

            # Target key electricity planning documents
            is_relevant_doc = any(kw in text_lower or kw in full_href_lower for kw in [
                "plan", "nep", "survey", "eps", "adequacy", "forecast", "demand",
                "perspective", "capacity", "data centre", "data center", "resource"
            ])

            if is_relevant_doc and any(ext in full_href_lower for ext in [".pdf", ".xlsx", ".zip", "division", "report"]):
                # Extract year/date if available
                date_match = re.search(r"/(20\d{2})/(?:(\d{2})/)?", full_href)
                pub_date = date_match.group(1) if date_match else "Official CEA Publication"

                records.append({
                    "headline": title_text,
                    "publisher": "Central Electricity Authority (CEA)",
                    "publication_date": pub_date,
                    "document_url": full_href,
                    "query_matched": f"CEA Page: {section_name}",
                    "date_scraped": today_str,
                    "notes": f"CEA Official Planning Document from {section_name}",
                })

    except Exception as e:
        logger.warning(f"Error scanning CEA reports page {page_url}: {e}")

    return records


def update_projections_log(new_records: list[dict], existing_file: str) -> pd.DataFrame:
    """Append new official projections to log and deduplicate by document URL."""
    all_dfs = []
    if os.path.exists(existing_file):
        try:
            existing_df = pd.read_csv(existing_file)
            if not existing_df.empty:
                all_dfs.append(existing_df)
                logger.info(f"Loaded {len(existing_df)} existing records from {existing_file}")
        except Exception as e:
            logger.warning(f"Could not read existing projections log {existing_file}: {e}")

    if new_records:
        new_df = pd.DataFrame(new_records)
        all_dfs.append(new_df)

    if not all_dfs:
        return pd.DataFrame(columns=PROJECTION_COLUMNS)

    combined_df = pd.concat(all_dfs, ignore_index=True)

    for col in PROJECTION_COLUMNS:
        if col not in combined_df.columns:
            combined_df[col] = "Not disclosed"
        else:
            combined_df[col] = combined_df[col].apply(clean_text)

    # Deduplicate by document_url
    initial_count = len(combined_df)
    deduped_df = combined_df.drop_duplicates(subset=["document_url"], keep="first")
    duplicates_removed = initial_count - len(deduped_df)
    logger.info(f"Deduplication: {duplicates_removed} duplicate records removed, {len(deduped_df)} retained.")

    return deduped_df[PROJECTION_COLUMNS]


def run_official_projections_scraper() -> int:
    """Execute official demand projection monitor across PIB and CEA targets."""
    logger.info("=== Starting Official Demand Projection Monitor Scraper ===")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_records = []

    # 1. Government RSS queries (PIB / CEA)
    for query in GOV_RSS_QUERIES:
        records = scrape_pib_government_rss(query)
        all_records.extend(records)

    # 2. CEA Monitored Planning Pages
    for page_url, section_name in CEA_MONITORED_PAGES:
        records = scrape_cea_reports_directory(page_url, section_name)
        all_records.extend(records)

    # Combine, deduplicate, and save
    final_df = update_projections_log(all_records, OUTPUT_FILE)
    final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    logger.info(f"Successfully saved {len(final_df)} official projections to {OUTPUT_FILE}")

    return len(final_df)


if __name__ == "__main__":
    count = run_official_projections_scraper()
    print(f"\nCompleted official projections monitoring. Total documents logged: {count}")
