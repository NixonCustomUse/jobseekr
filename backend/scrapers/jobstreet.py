import re
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class JobStreetScraper(BaseScraper):
    BASE_URL = "https://www.jobstreet.com.my"

    def search_jobs(self, keyword="餐饮", location="Malaysia", page=1):
        params = {
            "keywords": keyword,
            "location": location,
            "page": page,
            "sort": "modified_date",
        }
        try:
            resp = requests.get(
                f"{self.BASE_URL}/en/job-search/job-vacancy.php",
                params=params,
                headers=self.headers,
                timeout=30,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error("JobStreet search failed: %s", e)
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        jobs = []
        for card in soup.select("[data-job-id]"):
            jobs.append(self._parse_card(card))
        return jobs

    def get_job_detail(self, url):
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error("JobStreet detail failed: %s", e)
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        desc_div = soup.select_one("[data-automation='jobDescription']")
        description = desc_div.get_text(strip=True) if desc_div else ""
        return {"description": description}

    def _parse_card(self, card):
        title_el = card.select_one("[data-automation='jobTitle']")
        company_el = card.select_one("[data-automation='jobCompany']")
        location_el = card.select_one("[data-automation='jobLocation']")
        url_el = card.select_one("a[href*='/en/job/']")

        url = ""
        if url_el:
            href = url_el.get("href", "")
            url = href if href.startswith("http") else f"{self.BASE_URL}{href}"

        posted_text = card.get_text()
        posted_at = None
        for pattern in [r"(\d+)\s+(min|hour|day|week|month)s?\s+ago",
                         r"Posted\s+(\d+)\s+(min|hour|day|week|month)s?\s+ago"]:
            m = re.search(pattern, posted_text, re.IGNORECASE)
            if m:
                posted_at = self._relative_to_date(int(m.group(1)), m.group(2))
                break

        return {
            "platform_id": card.get("data-job-id"),
            "title": title_el.get_text(strip=True) if title_el else "",
            "company": company_el.get_text(strip=True) if company_el else "",
            "location": location_el.get_text(strip=True) if location_el else "",
            "url": url,
            "posted_at": posted_at,
        }

    @staticmethod
    def _relative_to_date(amount, unit):
        now = datetime.utcnow()
        unit = unit.lower()
        if unit in ("min", "mins", "minute", "minutes"):
            return now.replace(second=0, microsecond=0).isoformat()
        elif unit in ("hour", "hours"):
            return now.replace(second=0, microsecond=0).isoformat()
        elif unit in ("day", "days"):
            return now.isoformat()
        elif unit in ("week", "weeks"):
            return now.isoformat()
        elif unit in ("month", "months"):
            return now.isoformat()
        return now.isoformat()
