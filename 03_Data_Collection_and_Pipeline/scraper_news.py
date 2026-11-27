"""
News & Announcement Monitor Scraper (India Data Centers)
Part of India AI Data Center Energy Demand Study

Purpose:
Monitors news sources via Google News RSS feeds for commissioning timelines,
investments, capacity announcements, and AI data center projects across India.

Output Schema (news_log.csv):
headline, source, publication_date, url, query_matched, date_scraped
"""

import os
import sys
import time
import logging
from datetime import datetime
from urllib.parse import quote_plus

import feedparser
import pandas as pd
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("scraper_news")

USER_AGENT = "AcademicResearch-IndiaDC/1.0 (+https://github.com/dissertation-dc-india; contact: academic.dc.research@gmail.com)"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

RATE_LIMIT_DELAY = 2.5  # Seconds between requests

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "news_log.csv")

NEWS_COLUMNS = [
    "headline",
    "source",
    "publication_date",
    "url",
    "query_matched",
    "date_scraped",
]

DEFAULT_QUERIES = [
    '"data center" India AI',
    '"data centre" India investment',
    "hyperscale India MW",
    '"Google Adani" data center',
    '"Reliance Jamnagar" AI',
    '"Yotta" data center India',
    '"CtrlS" data center expansion',
    '"NTT" data center India',
    '"Microsoft" data center India',
    '"AWS" data center India',
    'India data center electricity demand "GW"',
    '"Green Open Access" data center India',
]


def clean_text(text: str) -> str:
    """Clean and standardize text field."""
    if not text:
        return "Not disclosed"
    s = " ".join(str(text).split())
    return s if s else "Not disclosed"


def fetch_google_news_rss(query: str) -> list[dict]:
    """Fetch and parse Google News RSS feed for a specific search query."""
    records = []
    encoded_query = quote_plus(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    logger.info(f"Querying RSS for: '{query}' -> {rss_url}")
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(rss_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Google News RSS returned HTTP {resp.status_code} for query: {query}")
            return records

        feed = feedparser.parse(resp.content)
        if feed.bozo:
            logger.debug(f"Feedparser note for '{query}': {feed.bozo_exception}")

        entries = feed.entries
        logger.info(f"Found {len(entries)} articles for query: '{query}'")

        for entry in entries:
            headline = clean_text(entry.get("title", ""))
            url = entry.get("link", "").strip()
            pub_date = entry.get("published", entry.get("updated", today_str))

            # Extract source name from entry.source or title suffix
            source_name = "Not disclosed"
            if "source" in entry and hasattr(entry.source, "title"):
                source_name = entry.source.title
            elif " - " in headline:
                source_name = headline.rsplit(" - ", 1)[-1].strip()

            records.append({
                "headline": headline,
                "source": clean_text(source_name),
                "publication_date": clean_text(pub_date),
                "url": clean_text(url),
                "query_matched": query,
                "date_scraped": today_str,
            })

    except Exception as e:
        logger.warning(f"Error fetching RSS for query '{query}': {e}")

    return records


def update_news_log(new_records: list[dict], existing_file: str) -> pd.DataFrame:
    """
    Append new news records into the running news_log.csv,
    deduplicating by article URL.
    """
    all_dfs = []
    if os.path.exists(existing_file):
        try:
            existing_df = pd.read_csv(existing_file)
            if not existing_df.empty:
                all_dfs.append(existing_df)
                logger.info(f"Loaded {len(existing_df)} existing articles from {existing_file}")
        except Exception as e:
            logger.warning(f"Could not read existing news log {existing_file}: {e}")

    if new_records:
        new_df = pd.DataFrame(new_records)
        all_dfs.append(new_df)

    if not all_dfs:
        return pd.DataFrame(columns=NEWS_COLUMNS)

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Clean & ensure columns
    for col in NEWS_COLUMNS:
        if col not in combined_df.columns:
            combined_df[col] = "Not disclosed"
        else:
            combined_df[col] = combined_df[col].apply(clean_text)

    # Deduplicate by URL (keep earliest scraped or first seen)
    initial_count = len(combined_df)
    deduped_df = combined_df.drop_duplicates(subset=["url"], keep="first")
    duplicates_removed = initial_count - len(deduped_df)
    logger.info(f"Deduplication: {duplicates_removed} duplicate articles removed, {len(deduped_df)} retained.")

    return deduped_df[NEWS_COLUMNS]


def run_news_scraper(queries: list[str] = None) -> int:
    """Run news scraper across all targeted search queries."""
    if queries is None:
        queries = DEFAULT_QUERIES

    logger.info(f"=== Starting News & Announcement Scraper ({len(queries)} queries) ===")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_new_articles = []
    for query in queries:
        articles = fetch_google_news_rss(query)
        all_new_articles.extend(articles)

    final_df = update_news_log(all_new_articles, OUTPUT_FILE)
    final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    logger.info(f"Successfully saved {len(final_df)} articles to {OUTPUT_FILE}")

    return len(final_df)


if __name__ == "__main__":
    count = run_news_scraper()
    print(f"\nCompleted news monitoring. Total articles logged: {count}")
