"""
Multi-Source India Data Center Scraping Pipeline Orchestrator
Author: Dissertation Research Suite (Demand-Side AI DC Energy Modeling in India)

Executes all scrapers in sequence with rate-limiting, error isolation,
and comprehensive summary reporting:
1. scraper_facilities.py           -> Facility Directory (Location, Operator, Capacity MW, Status)
2. scraper_news.py                 -> Commissioning Timelines & Project Announcements
3. scraper_cea_emission_factor.py  -> CEA Grid CO2 Baseline Database Checker & Downloader
4. scraper_official_projections.py -> Government / CEA Electricity Demand Planning Monitor
"""

import os
import sys
import time
import logging
from datetime import datetime

# Import modular scrapers
import scraper_facilities
import scraper_news
import scraper_cea_emission_factor
import scraper_official_projections

# Configure Root Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "data", "pipeline_run.log"), encoding="utf-8"),
    ]
)
logger = logging.getLogger("run_all")

INTER_SCRAPER_PAUSE_SECONDS = 5.0  # Courtesy pause between different domain scrapers


def run_pipeline() -> dict:
    """Run all scrapers sequentially with isolated try-except blocks."""
    start_time = datetime.now()
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

    logger.info("=" * 70)
    logger.info("STARTING INDIA DATA CENTER DEMAND-SIDE DATA SCRAPING PIPELINE")
    logger.info(f"Execution started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)

    results = {}

    # -------------------------------------------------------------
    # 1. Scraper 1: Facilities Directory
    # -------------------------------------------------------------
    logger.info("\n>>> [1/4] Running Scraper 1: Facility Directory Scraper")
    try:
        t0 = time.time()
        facility_count = scraper_facilities.run_facility_scraper()
        duration = round(time.time() - t0, 2)
        results["facilities"] = {
            "status": "SUCCESS",
            "count": facility_count,
            "output_file": scraper_facilities.OUTPUT_FILE,
            "duration_sec": duration,
        }
    except Exception as e:
        logger.error(f"Facility scraper encountered an unhandled error: {e}", exc_info=True)
        results["facilities"] = {
            "status": "FAILED",
            "error": str(e),
            "output_file": scraper_facilities.OUTPUT_FILE,
            "duration_sec": 0,
        }

    logger.info(f"Inter-scraper pause: resting for {INTER_SCRAPER_PAUSE_SECONDS} seconds...")
    time.sleep(INTER_SCRAPER_PAUSE_SECONDS)

    # -------------------------------------------------------------
    # 2. Scraper 2: News & Announcement Monitor
    # -------------------------------------------------------------
    logger.info("\n>>> [2/4] Running Scraper 2: News & Announcements Monitor")
    try:
        t0 = time.time()
        news_count = scraper_news.run_news_scraper()
        duration = round(time.time() - t0, 2)
        results["news"] = {
            "status": "SUCCESS",
            "count": news_count,
            "output_file": scraper_news.OUTPUT_FILE,
            "duration_sec": duration,
        }
    except Exception as e:
        logger.error(f"News monitor encountered an unhandled error: {e}", exc_info=True)
        results["news"] = {
            "status": "FAILED",
            "error": str(e),
            "output_file": scraper_news.OUTPUT_FILE,
            "duration_sec": 0,
        }

    logger.info(f"Inter-scraper pause: resting for {INTER_SCRAPER_PAUSE_SECONDS} seconds...")
    time.sleep(INTER_SCRAPER_PAUSE_SECONDS)

    # -------------------------------------------------------------
    # 3. Scraper 3: CEA Grid Emission Factor Checker
    # -------------------------------------------------------------
    logger.info("\n>>> [3/4] Running Scraper 3: CEA Emission Factor Checker")
    try:
        t0 = time.time()
        cea_res = scraper_cea_emission_factor.run_cea_checker()
        duration = round(time.time() - t0, 2)
        results["cea_emission"] = {
            "status": "SUCCESS" if cea_res.get("status") == "success" else "WARNING",
            "version": cea_res.get("latest_version"),
            "is_new_version": cea_res.get("is_new_version"),
            "output_file": scraper_cea_emission_factor.LOG_FILE,
            "duration_sec": duration,
        }
    except Exception as e:
        logger.error(f"CEA emission factor checker encountered an unhandled error: {e}", exc_info=True)
        results["cea_emission"] = {
            "status": "FAILED",
            "error": str(e),
            "output_file": scraper_cea_emission_factor.LOG_FILE,
            "duration_sec": 0,
        }

    logger.info(f"Inter-scraper pause: resting for {INTER_SCRAPER_PAUSE_SECONDS} seconds...")
    time.sleep(INTER_SCRAPER_PAUSE_SECONDS)

    # -------------------------------------------------------------
    # 4. Scraper 4: Official Demand Projection Monitor
    # -------------------------------------------------------------
    logger.info("\n>>> [4/4] Running Scraper 4: Official Demand Projection Monitor")
    try:
        t0 = time.time()
        proj_count = scraper_official_projections.run_official_projections_scraper()
        duration = round(time.time() - t0, 2)
        results["official_projections"] = {
            "status": "SUCCESS",
            "count": proj_count,
            "output_file": scraper_official_projections.OUTPUT_FILE,
            "duration_sec": duration,
        }
    except Exception as e:
        logger.error(f"Official projections monitor encountered an unhandled error: {e}", exc_info=True)
        results["official_projections"] = {
            "status": "FAILED",
            "error": str(e),
            "output_file": scraper_official_projections.OUTPUT_FILE,
            "duration_sec": 0,
        }

    # -------------------------------------------------------------
    # Summary Dashboard
    # -------------------------------------------------------------
    total_duration = round((datetime.now() - start_time).total_seconds(), 2)

    logger.info("\n" + "=" * 70)
    logger.info("PIPELINE EXECUTION SUMMARY REPORT")
    logger.info("=" * 70)
    for scraper_name, res in results.items():
        status_symbol = "[OK]" if res["status"] == "SUCCESS" else "[!]"
        logger.info(
            f"{status_symbol} {scraper_name.upper():<22} | "
            f"Status: {res['status']:<7} | "
            f"Duration: {res.get('duration_sec', 0):>5.1f}s | "
            f"Details: {res.get('count', res.get('version', 'N/A'))}"
        )
    logger.info(f"Total Pipeline Runtime: {total_duration}s")
    logger.info(f"All outputs saved under directory: {os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))}")
    logger.info("=" * 70)

    return results


if __name__ == "__main__":
    run_pipeline()
