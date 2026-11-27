"""
Data Center Facility Directory Scraper (India)
Part of India AI Data Center Energy Demand Study

Target Sources:
- Wikipedia (Data centre industry in India, state lists, city lists)
- AI Data Center Index (aidatacenterindex.com) - AI-specific facilities & capacities
- DataCenterMap.com (datacentermap.com/india/) - Directory listings (with graceful fallback)

Output Schema:
facility_name, operator, state, city, capacity_mw, capacity_source_note, workload_type, status, source_url, source_name, date_scraped
"""

import os
import re
import sys
import time
import logging
from datetime import datetime
from io import StringIO
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
logger = logging.getLogger("scraper_facilities")

USER_AGENT = "AcademicResearch-IndiaDC/1.0 (+https://github.com/dissertation-dc-india; contact: academic.dc.research@gmail.com)"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

RATE_LIMIT_DELAY = 2.5  # Seconds between requests to same domain

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "facilities.csv")

FACILITY_COLUMNS = [
    "facility_name",
    "operator",
    "state",
    "city",
    "capacity_mw",
    "capacity_source_note",
    "workload_type",
    "status",
    "source_url",
    "source_name",
    "date_scraped",
]


def clean_field(val: any, default: str = "Not disclosed") -> str:
    """Normalize string fields and ensure non-empty valid strings."""
    if val is None or pd.isna(val):
        return default
    s = str(val).strip()
    s = re.sub(r"\[\d+\]", "", s)  # remove wikipedia citations like [1], [2]
    s = re.sub(r"\s+", " ", s)
    if not s or s.lower() in ["nan", "none", "null", "n/a", "-", "--", ""]:
        return default
    return s


def normalize_status(val: str) -> str:
    """Normalize status to controlled vocabulary."""
    if not val or val == "Not disclosed":
        return "unknown"
    s = str(val).lower().strip()
    if "operational" in s or "active" in s or "live" in s:
        return "operational"
    elif "under construction" in s or "construction" in s:
        return "under_construction"
    elif "planned" in s or "proposed" in s:
        return "planned"
    elif "announced" in s:
        return "announced"
    elif "evaluation" in s or "evaluating" in s:
        return "under_evaluation"
    return "unknown"


def parse_mw_capacity(text: str) -> tuple[float | None, str]:
    """Extract numeric capacity in MW (as float) and note from text if present."""
    if not text or text == "Not disclosed":
        return None, "Not disclosed"
    
    # Check for MW pattern
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:MW|megawatt|Mega Watt)", text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1)), clean_field(text)
        except ValueError:
            pass
    
    # Check for GW pattern
    match_gw = re.search(r"(\d+(?:\.\d+)?)\s*(?:GW|gigawatt)", text, re.IGNORECASE)
    if match_gw:
        try:
            mw = float(match_gw.group(1)) * 1000.0
            return float(mw), clean_field(text)
        except Exception:
            pass

    return None, clean_field(text)



def scrape_wikipedia_west_bengal() -> list[dict]:
    """Scrape List of data centres in West Bengal Wikipedia page."""
    records = []
    url = "https://en.wikipedia.org/wiki/List_of_data_centres_in_West_Bengal"
    logger.info(f"Scraping Wikipedia: {url}")
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch {url} (HTTP {resp.status_code})")
            return records

        tables = pd.read_html(StringIO(resp.text))
        if not tables:
            logger.warning(f"No tables found on {url}")
            return records

        df = tables[0]
        logger.info(f"Loaded West Bengal table with {len(df)} rows")

        for _, row in df.iterrows():
            city = clean_field(row.get("City/ metropolitan area") or row.get("Location"))
            operator = clean_field(row.get("Provider/ Operator") or row.get("Operator"))
            details = clean_field(row.get("Details"))
            location = clean_field(row.get("Location"))
            status = normalize_status(clean_field(row.get("Status")))

            facility_name = operator
            if location != "Not disclosed" and location != city:
                facility_name = f"{operator} ({location})"

            cap_mw, cap_note = parse_mw_capacity(details)

            workload = "General / Cloud"
            if "ai" in details.lower() or "gpu" in details.lower():
                workload = "AI / High Performance Compute"

            records.append({
                "facility_name": clean_field(facility_name),
                "operator": operator,
                "state": "West Bengal",
                "city": city,
                "capacity_mw": cap_mw if cap_mw is not None else "Not disclosed",
                "capacity_source_note": cap_note if cap_note != "Not disclosed" else "Wikipedia List of data centres in West Bengal",
                "workload_type": workload,
                "status": status,
                "source_url": url,
                "source_name": "Wikipedia: List of data centres in West Bengal",
                "date_scraped": today_str,
            })
    except Exception as e:
        logger.warning(f"Error scraping Wikipedia West Bengal: {e}")

    return records


def scrape_wikipedia_industry_india() -> list[dict]:
    """Scrape Data centre industry in India Wikipedia page."""
    records = []
    url = "https://en.wikipedia.org/wiki/Data_centre_industry_in_India"
    logger.info(f"Scraping Wikipedia: {url}")
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch {url} (HTTP {resp.status_code})")
            return records

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Check all tables and text paragraphs for operator hubs
        # Parse major players and hubs mentioned in article body
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return records

        # Look for list elements or bold operator names
        paragraphs = content_div.find_all(["p", "li"])
        major_cities = {
            "mumbai": ("Maharashtra", "Mumbai"),
            "navi mumbai": ("Maharashtra", "Navi Mumbai"),
            "chennai": ("Tamil Nadu", "Chennai"),
            "hyderabad": ("Telangana", "Hyderabad"),
            "bengaluru": ("Karnataka", "Bengaluru"),
            "bangalore": ("Karnataka", "Bengaluru"),
            "noida": ("Uttar Pradesh", "Noida"),
            "greater noida": ("Uttar Pradesh", "Greater Noida"),
            "pune": ("Maharashtra", "Pune"),
            "delhi": ("Delhi NCR", "Delhi"),
            "kolkata": ("West Bengal", "Kolkata"),
            "kochi": ("Kerala", "Kochi"),
            "vizag": ("Andhra Pradesh", "Visakhapatnam"),
            "visakhapatnam": ("Andhra Pradesh", "Visakhapatnam"),
            "chandigarh": ("Punjab", "Chandigarh"),
            "jaipur": ("Rajasthan", "Jaipur"),
        }

        known_operators = [
            "NTT", "CtrlS", "Yotta", "Sify", "STT GDC", "AdaniConneX", "Equinix",
            "DigitalConnex", "Nxtra", "Airtel Nxtra", "Web Werks", "Iron Mountain",
            "CapitaLand", "Princeton Digital Group", "PDG", "Colt DCS", "RackBank",
            "ESR", "Reliance Jio", "Tata Communications", "Bridge Data Centres"
        ]

        for p in paragraphs:
            text = p.get_text()
            matched_op = None
            for op in known_operators:
                if re.search(rf"\b{re.escape(op)}\b", text, re.IGNORECASE):
                    matched_op = op
                    break
            
            if matched_op:
                matched_city = None
                matched_state = "Not disclosed"
                text_lower = text.lower()
                for c_key, (st, ct) in major_cities.items():
                    if c_key in text_lower:
                        matched_city = ct
                        matched_state = st
                        break
                
                if matched_city:
                    cap_mw, cap_note = parse_mw_capacity(text)
                    status = "operational"
                    if any(w in text_lower for w in ["planned", "proposed", "upcoming", "under construction", "investing"]):
                        status = "announced" if "planned" in text_lower or "proposed" in text_lower else "under_construction"
                    
                    workload = "General / Cloud"
                    if "ai" in text_lower or "gpu" in text_lower:
                        workload = "AI / High Performance Compute"

                    records.append({
                        "facility_name": f"{matched_op} Data Center ({matched_city})",
                        "operator": matched_op,
                        "state": matched_state,
                        "city": matched_city,
                        "capacity_mw": cap_mw if cap_mw is not None else "Not disclosed",
                        "capacity_source_note": cap_note if cap_note != "Not disclosed" else "Wikipedia Data centre industry in India",
                        "workload_type": workload,
                        "status": normalize_status(status),
                        "source_url": url,
                        "source_name": "Wikipedia: Data centre industry in India",
                        "date_scraped": today_str,
                    })

    except Exception as e:
        logger.warning(f"Error scraping Wikipedia Data centre industry in India: {e}")

    return records


def scrape_aidatacenterindex() -> list[dict]:
    """
    Scrape AI Data Center Index (aidatacenterindex.com) for India facilities.
    Extracts capacity (MW), status, operator, workload, and location.
    """
    records = []
    base_url = "https://aidatacenterindex.com"
    sitemap_url = "https://aidatacenterindex.com/sitemap.xml"
    logger.info(f"Querying AI Data Center Index sitemap: {sitemap_url}")
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(sitemap_url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch {sitemap_url} (HTTP {resp.status_code})")
            return records

        # Find datacenter URLs targeting India
        raw_locs = re.findall(r"<loc>(https://aidatacenterindex\.com/datacenters/[^<]+)</loc>", resp.text)
        
        # Filter for India-specific keywords or slug names
        india_slugs = []
        for loc in raw_locs:
            loc_lower = loc.lower()
            if any(k in loc_lower for k in [
                "india", "jamnagar", "noida", "mumbai", "hyderabad", "bengaluru",
                "chennai", "airawat", "yotta", "vizag", "pune", "telangana", "adani"
            ]):
                # Avoid US states like indiana
                if "indiana" in loc_lower and "india" not in loc_lower.replace("indiana", ""):
                    continue
                india_slugs.append(loc)

        logger.info(f"Found {len(india_slugs)} India AI data center URLs on aidatacenterindex.com")

        for dc_url in india_slugs:
            time.sleep(RATE_LIMIT_DELAY)
            try:
                r_dc = requests.get(dc_url, headers=HEADERS, timeout=15)
                r_dc.encoding = "utf-8"
                if r_dc.status_code != 200:
                    logger.warning(f"Could not retrieve {dc_url} (HTTP {r_dc.status_code})")
                    continue

                soup = BeautifulSoup(r_dc.text, "html.parser")
                h1 = soup.find("h1")
                facility_title = h1.get_text(strip=True) if h1 else "AI Data Center"

                # Parse definition lists <dt> / <dd> or structured paragraphs
                dt_map = {}
                for dt, dd in zip(soup.find_all("dt"), soup.find_all("dd")):
                    dt_map[dt.get_text(strip=True).lower()] = dd.get_text(strip=True)

                all_text = soup.get_text(separator=" ", strip=True)

                # Extract Capacity MW
                capacity_mw = None
                capacity_note = "Not disclosed"
                cap_match = re.search(r"(\d+(?:\.\d+)?)\s*MW", all_text, re.IGNORECASE)
                if cap_match:
                    try:
                        capacity_mw = float(cap_match.group(1))
                    except ValueError:
                        capacity_mw = None
                    capacity_note = f"aidatacenterindex tracking ({cap_match.group(0)})"
                elif re.search(r"(\d+(?:\.\d+)?)\s*GW", all_text, re.IGNORECASE):
                    gw_m = re.search(r"(\d+(?:\.\d+)?)\s*GW", all_text, re.IGNORECASE)
                    try:
                        capacity_mw = float(gw_m.group(1)) * 1000.0
                    except ValueError:
                        capacity_mw = None
                    capacity_note = f"aidatacenterindex tracking ({gw_m.group(0)})"

                # Extract Operator
                operator = "Not disclosed"
                for dt_k, dd_v in dt_map.items():
                    if "operator" in dt_k or "who operates" in dt_k:
                        operator = dd_v.split("is operated by")[-1].split(".")[0].strip() if "is operated by" in dd_v else dd_v
                        break
                if operator == "Not disclosed":
                    if "Yotta" in facility_title:
                        operator = "Yotta Data Services"
                    elif "Reliance" in facility_title or "Jio" in facility_title:
                        operator = "Reliance Jio / Meta"
                    elif "Google" in facility_title and "Adani" in facility_title:
                        operator = "Google / AdaniConneX"
                    elif "AWS" in facility_title or "Amazon" in facility_title:
                        operator = "Amazon Web Services (AWS)"
                    elif "Microsoft" in facility_title:
                        operator = "Microsoft Azure"
                    elif "Oracle" in facility_title:
                        operator = "Oracle Cloud"
                    elif "NTT" in facility_title:
                        operator = "NTT Data"
                    elif "AIRAWAT" in facility_title:
                        operator = "C-DAC / MeitY"

                # Extract Location (City, State)
                city = "Not disclosed"
                state = "Not disclosed"
                location_patterns = [
                    (r"Greater Noida", "Greater Noida", "Uttar Pradesh"),
                    (r"Noida", "Noida", "Uttar Pradesh"),
                    (r"Jamnagar", "Jamnagar", "Gujarat"),
                    (r"Visakhapatnam|Vizag", "Visakhapatnam", "Andhra Pradesh"),
                    (r"Hyderabad", "Hyderabad", "Telangana"),
                    (r"Telangana", "Hyderabad", "Telangana"),
                    (r"Mumbai", "Mumbai", "Maharashtra"),
                    (r"Navi Mumbai", "Navi Mumbai", "Maharashtra"),
                    (r"Pune", "Pune", "Maharashtra"),
                    (r"Bengaluru|Bangalore", "Bengaluru", "Karnataka"),
                    (r"Chennai", "Chennai", "Tamil Nadu"),
                    (r"Delhi", "Delhi", "Delhi NCR"),
                    (r"Kolkata", "Kolkata", "West Bengal"),
                ]
                for pat, ct, st in location_patterns:
                    if re.search(pat, facility_title + " " + all_text, re.IGNORECASE):
                        city = ct
                        state = st
                        break

                # Extract Status
                status = "unknown"
                for dt_k, dd_v in dt_map.items():
                    if "status" in dt_k:
                        status = normalize_status(dd_v)
                        break
                if status == "unknown":
                    if "under construction" in all_text.lower():
                        status = "under_construction"
                    elif "operational" in all_text.lower() or "live" in all_text.lower():
                        status = "operational"
                    elif "announced" in all_text.lower() or "planned" in all_text.lower():
                        status = "announced"

                # Extract Workload Type
                workload = "AI / GPU Compute"
                if "training" in all_text.lower():
                    workload = "AI Model Training / LLM Supercomputing"
                elif "inference" in all_text.lower():
                    workload = "AI Inference & Cloud Workloads"

                records.append({
                    "facility_name": clean_field(facility_title),
                    "operator": clean_field(operator),
                    "state": clean_field(state),
                    "city": clean_field(city),
                    "capacity_mw": capacity_mw if capacity_mw is not None else "Not disclosed",
                    "capacity_source_note": clean_field(capacity_note),
                    "workload_type": clean_field(workload),
                    "status": normalize_status(status),
                    "source_url": dc_url,
                    "source_name": "AI Data Center Index",
                    "date_scraped": today_str,
                })
                logger.info(f"Extracted AI facility: {facility_title} ({city}, {capacity_mw})")
            except Exception as e:
                logger.warning(f"Error parsing facility page {dc_url}: {e}")

    except Exception as e:
        logger.warning(f"Error scraping aidatacenterindex: {e}")

    return records


def scrape_datacentermap_india() -> list[dict]:
    """
    Scrape DataCenterMap.com India directory.
    Degrades gracefully if protected by security challenge (Vercel/Cloudflare).
    """
    records = []
    url = "https://www.datacentermap.com/india/"
    logger.info(f"Attempting to query DataCenterMap: {url}")
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        time.sleep(RATE_LIMIT_DELAY)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = "utf-8"
        if resp.status_code == 429 or resp.status_code == 403 or "Security Checkpoint" in resp.text:
            logger.warning(
                f"DataCenterMap returned HTTP {resp.status_code} (Anti-bot / Vercel Security Checkpoint). "
                "Degrading gracefully and skipping direct HTML parsing for this run as per ground rules."
            )
            return records

        soup = BeautifulSoup(resp.text, "html.parser")
        listings = soup.find_all("div", class_=re.compile(r"listing|facility|datacenter", re.I))
        logger.info(f"Found {len(listings)} listings on DataCenterMap")

        for item in listings:
            name_elem = item.find(["h2", "h3", "h4", "a"])
            name = name_elem.get_text(strip=True) if name_elem else "Not disclosed"
            
            records.append({
                "facility_name": clean_field(name),
                "operator": "Not disclosed",
                "state": "Not disclosed",
                "city": "Not disclosed",
                "capacity_mw": "Not disclosed",
                "capacity_source_note": "Not disclosed",
                "workload_type": "General / Colocation",
                "status": "operational",
                "source_url": url,
                "source_name": "DataCenterMap India",
                "date_scraped": today_str,
            })
    except Exception as e:
        logger.warning(f"Graceful degradation on DataCenterMap scraper: {e}")

    return records


def deduplicate_facilities(new_records: list[dict], existing_file: str) -> pd.DataFrame:
    """
    Combine and deduplicate facilities across sources based on
    normalized (operator, city, facility_name).
    """
    all_dfs = []
    if os.path.exists(existing_file):
        try:
            existing_df = pd.read_csv(existing_file)
            if not existing_df.empty:
                all_dfs.append(existing_df)
                logger.info(f"Loaded {len(existing_df)} existing records from {existing_file}")
        except Exception as e:
            logger.warning(f"Could not read existing CSV {existing_file}: {e}")

    if new_records:
        new_df = pd.DataFrame(new_records)
        all_dfs.append(new_df)

    if not all_dfs:
        return pd.DataFrame(columns=FACILITY_COLUMNS)

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Ensure all columns present
    for col in FACILITY_COLUMNS:
        if col not in combined_df.columns:
            combined_df[col] = "Not disclosed"
        else:
            combined_df[col] = combined_df[col].apply(clean_field)

    # Clean deduplication key
    combined_df["_dedup_key"] = (
        combined_df["operator"].str.lower().str.replace(r"[^\w\s]", "", regex=True) + "_" +
        combined_df["city"].str.lower().str.replace(r"[^\w\s]", "", regex=True) + "_" +
        combined_df["facility_name"].str.lower().str.replace(r"[^\w\s]", "", regex=True)
    )

    # Prioritize records with known capacity and richer metadata
    def score_record(row):
        score = 0
        if row["capacity_mw"] != "Not disclosed":
            score += 10
        if row["status"] != "Not disclosed":
            score += 3
        if row["state"] != "Not disclosed":
            score += 2
        if "AI" in str(row["workload_type"]):
            score += 5
        return score

    combined_df["_score"] = combined_df.apply(score_record, axis=1)
    combined_df = combined_df.sort_values(by="_score", ascending=False)
    deduped_df = combined_df.drop_duplicates(subset=["_dedup_key"], keep="first")
    deduped_df = deduped_df.drop(columns=["_dedup_key", "_score"])

    return deduped_df[FACILITY_COLUMNS]


def run_facility_scraper(target_output_file: str = OUTPUT_FILE) -> int:
    """Execute all facility directory scrapers and save results to CSV."""
    logger.info("=== Starting Data Center Facility Directory Scraper ===")
    os.makedirs(os.path.dirname(target_output_file) or ".", exist_ok=True)

    all_records = []

    # 1. Wikipedia West Bengal
    wb_records = scrape_wikipedia_west_bengal()
    logger.info(f"Scraped {len(wb_records)} facilities from Wikipedia West Bengal")
    all_records.extend(wb_records)

    # 2. Wikipedia Industry India Overview
    ind_records = scrape_wikipedia_industry_india()
    logger.info(f"Scraped {len(ind_records)} facilities from Wikipedia India Overview")
    all_records.extend(ind_records)

    # 3. AI Data Center Index
    ai_records = scrape_aidatacenterindex()
    logger.info(f"Scraped {len(ai_records)} AI facilities from AI Data Center Index")
    all_records.extend(ai_records)

    # 4. DataCenterMap
    dcm_records = scrape_datacentermap_india()
    logger.info(f"Scraped {len(dcm_records)} facilities from DataCenterMap")
    all_records.extend(dcm_records)

    # Deduplicate and save
    final_df = deduplicate_facilities(all_records, target_output_file)
    final_df.to_csv(target_output_file, index=False, encoding="utf-8-sig")
    logger.info(f"Successfully saved {len(final_df)} unique facilities to {target_output_file}")

    return len(final_df)


if __name__ == "__main__":
    count = run_facility_scraper()
    print(f"\nCompleted facility scraping. Total tracked facilities: {count}")
