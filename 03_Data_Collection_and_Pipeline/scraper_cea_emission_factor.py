"""
CEA Grid Emission Factor Checker
Part of India AI Data Center Energy Demand Study

Target:
Central Electricity Authority (CEA) CDM CO2 Baseline Database
URL: https://cea.nic.in/cdm-co2-baseline-database/?lang=en

Approach:
- Scrape the CEA CO2 database page for the latest version number (e.g. Version 22.0) and files.
- Compare against last-known version in data/last_known_version.txt.
- Download the new Excel/PDF dataset to data/cea_downloads/ if a new version is available.
- Log record to data/cea_emission_factor_log.csv.
"""

import os
import re
import sys
import time
import logging
from datetime import datetime
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("scraper_cea_emission_factor")

USER_AGENT = "AcademicResearch-IndiaDC/1.0 (+https://github.com/dissertation-dc-india; contact: academic.dc.research@gmail.com)"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

RATE_LIMIT_DELAY = 2.5

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
DOWNLOADS_DIR = os.path.join(OUTPUT_DIR, "cea_downloads")
VERSION_FILE = os.path.join(OUTPUT_DIR, "last_known_version.txt")
LOG_FILE = os.path.join(OUTPUT_DIR, "cea_emission_factor_log.csv")

CEA_PAGE_URL = "https://cea.nic.in/cdm-co2-baseline-database/?lang=en"

CEA_COLUMNS = [
    "version",
    "publication_date",
    "file_name",
    "file_url",
    "download_status",
    "date_scraped",
    "notes",
]


def clean_text(text: str) -> str:
    if not text:
        return "Not disclosed"
    return " ".join(str(text).split())


def get_last_known_version() -> str:
    """Read the last recorded version string from local text file."""
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            logger.warning(f"Could not read {VERSION_FILE}: {e}")
    return "None"


def save_last_known_version(version_str: str) -> None:
    """Save the latest recorded version string to local file."""
    try:
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            f.write(version_str.strip())
        logger.info(f"Updated {VERSION_FILE} to '{version_str.strip()}'")
    except Exception as e:
        logger.warning(f"Could not save version to {VERSION_FILE}: {e}")


def download_file(url: str, dest_folder: str) -> tuple[str, bool]:
    """Download file from URL to destination directory."""
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.basename(url.split("?")[0])
    if not filename:
        filename = "cea_database_download.bin"
    dest_path = os.path.join(dest_folder, filename)

    try:
        logger.info(f"Downloading {url} -> {dest_path}")
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        if resp.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logger.info(f"Downloaded successfully: {filename} ({os.path.getsize(dest_path)} bytes)")
            return filename, True
        else:
            logger.warning(f"Download failed with status {resp.status_code}")
            return filename, False
    except Exception as e:
        logger.warning(f"Error downloading {url}: {e}")
        return filename, False


def scrape_cea_database() -> dict:
    """Scrape CEA CO2 Baseline Database page to detect latest versions."""
    logger.info(f"Fetching CEA CO2 Baseline Database page: {CEA_PAGE_URL}")
    today_str = datetime.now().strftime("%Y-%m-%d")

    result = {
        "latest_version": "Not disclosed",
        "versions_found": [],
        "download_links": [],
        "success": False,
    }

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(CEA_PAGE_URL, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch CEA page (HTTP {resp.status_code})")
            return result

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Look for version patterns (e.g. Version 22.0, Version 21.0, Version 20.0)
        all_links = soup.find_all("a")
        
        version_records = []
        for a in all_links:
            href = a.get("href", "")
            text = a.get_text(strip=True)
            if not href:
                continue

            full_href = urljoin(CEA_PAGE_URL, href)
            
            # Check if this link is an excel, pdf, or zip file of the database
            is_db_file = any(ext in full_href.lower() for ext in [".xlsx", ".xls", ".pdf", ".zip"])
            
            v_match = re.search(r"(?:Version|Ver\.?|V)\s*(\d+(?:\.\d+)?)", text + " " + full_href, re.IGNORECASE)
            if v_match and is_db_file:
                v_num = float(v_match.group(1))
                v_label = f"Version {v_match.group(1)}"
                
                # Check for publication year in URL path (e.g. /2026/09/ or /2025/12/)
                date_match = re.search(r"/(\d{4})/(\d{2})/", full_href)
                pub_date = f"{date_match.group(1)}-{date_match.group(2)}" if date_match else "Not disclosed"

                version_records.append({
                    "version_num": v_num,
                    "version_label": v_label,
                    "link_text": text,
                    "url": full_href,
                    "publication_date": pub_date,
                    "file_ext": os.path.splitext(full_href)[1],
                })

        if version_records:
            # Sort by version number descending
            version_records.sort(key=lambda x: x["version_num"], reverse=True)
            result["latest_version"] = version_records[0]["version_label"]
            result["versions_found"] = version_records
            result["success"] = True
            logger.info(f"Latest CEA CO2 Baseline Database identified: {result['latest_version']}")
        else:
            logger.warning("No version records matched on CEA page.")

    except Exception as e:
        logger.warning(f"Error scraping CEA page: {e}")

    return result


def run_cea_checker() -> dict:
    """
    Main function for CEA Emission Factor scraper.
    Checks for updates, downloads files when new, and maintains log.
    """
    logger.info("=== Starting CEA CO2 Baseline Emission Factor Checker ===")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    last_version = get_last_known_version()
    logger.info(f"Last-known version on record: '{last_version}'")

    cea_data = scrape_cea_database()
    if not cea_data["success"]:
        logger.warning("Could not parse CEA versions. Exiting checker gracefully.")
        return {"status": "failed", "latest_version": last_version}

    latest_version = cea_data["latest_version"]
    logger.info(f"Discovered online latest version: '{latest_version}'")

    new_records = []
    is_new_version = (latest_version != last_version)

    # Process all links belonging to the latest version
    top_version_links = [
        rec for rec in cea_data["versions_found"]
        if rec["version_label"] == latest_version
    ]

    for item in top_version_links:
        file_url = item["url"]
        fname = os.path.basename(file_url.split("?")[0])
        local_target = os.path.join(DOWNLOADS_DIR, fname)
        
        # Download if file doesn't exist locally or if it's a new version
        download_status = "Already exists"
        if not os.path.exists(local_target) or is_new_version:
            _, success = download_file(file_url, DOWNLOADS_DIR)
            download_status = "Downloaded successfully" if success else "Download failed"

        new_records.append({
            "version": item["version_label"],
            "publication_date": item["publication_date"],
            "file_name": fname,
            "file_url": file_url,
            "download_status": download_status,
            "date_scraped": today_str,
            "notes": f"CEA Official CDM Baseline Database document ({item['link_text']})",
        })

    # Update log CSV
    all_dfs = []
    if os.path.exists(LOG_FILE):
        try:
            existing_df = pd.read_csv(LOG_FILE)
            if not existing_df.empty:
                all_dfs.append(existing_df)
        except Exception as e:
            logger.warning(f"Error reading {LOG_FILE}: {e}")

    if new_records:
        all_dfs.append(pd.DataFrame(new_records))

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        for col in CEA_COLUMNS:
            if col not in combined_df.columns:
                combined_df[col] = "Not disclosed"
        # Deduplicate on file_url and version
        deduped_df = combined_df.drop_duplicates(subset=["version", "file_url"], keep="last")
        deduped_df[CEA_COLUMNS].to_csv(LOG_FILE, index=False, encoding="utf-8")
        logger.info(f"Updated CEA emission log at {LOG_FILE}")

    # Update last_known_version.txt
    save_last_known_version(latest_version)

    return {
        "status": "success",
        "latest_version": latest_version,
        "is_new_version": is_new_version,
        "files_tracked": len(top_version_links),
    }


if __name__ == "__main__":
    res = run_cea_checker()
    print(f"\nCEA Checker Finished. Result: {res}")
