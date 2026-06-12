import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
DATABASE_PATH = os.path.join(BASE_DIR, "data.db")

CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-20250514"

SCRAPE_INTERVAL_HOURS = int(os.environ.get("SCRAPE_INTERVAL_HOURS", "6"))
SCRAPE_CATEGORY = "餐饮"  # JobStreet food & beverage category
SCRAPE_LOCATION = "Malaysia"
JOBSTREET_BASE_URL = "https://www.jobstreet.com.my"

SESSION_TYPE = "filesystem"
