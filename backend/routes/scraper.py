import logging

from flask import Blueprint, jsonify

from database import query, query_one, execute

logger = logging.getLogger(__name__)

scraper_bp = Blueprint("scraper", __name__)


def do_scrape():
    from scrapers.jobstreet import JobStreetScraper

    scraper = JobStreetScraper()
    jobs = scraper.search_jobs(keyword="餐饮", location="Malaysia")
    imported = 0
    for job in jobs:
        existing = query_one(
            "SELECT id FROM jobs WHERE platform_id = ?",
            [job.get("platform_id")],
        )
        if existing:
            continue
        execute(
            """INSERT INTO jobs
               (platform, platform_id, title, company, location, category, url, posted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                "jobstreet",
                job.get("platform_id"),
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                "餐饮",
                job.get("url", ""),
                job.get("posted_at"),
            ],
        )
        imported += 1
    logger.info("Scraped %d/%d jobs", imported, len(jobs))


@scraper_bp.route("/api/scrape/jobstreet", methods=["POST"])
def trigger_scrape():
    try:
        do_scrape()
        total = query("SELECT COUNT(*) as c FROM jobs")[0]["c"]
        return jsonify({"ok": True, "total_jobs": total})
    except Exception as e:
        logger.error("Scrape failed: %s", e)
        return jsonify({"error": str(e)}), 500


@scraper_bp.route("/api/scrape/status", methods=["GET"])
def scrape_status():
    total = query("SELECT COUNT(*) as c FROM jobs")[0]["c"]
    return jsonify({"total_jobs": total})
