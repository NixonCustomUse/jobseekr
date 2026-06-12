import logging
import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler

from config import SECRET_KEY, SCRAPE_INTERVAL_HOURS, BASE_DIR
from database import init_db
from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.profile import profile_bp
from routes.applications import applications_bp
from routes.scraper import scraper_bp

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

_frontend_dir = os.path.join(os.path.dirname(BASE_DIR), "frontend")
executor = ThreadPoolExecutor(max_workers=1)
scheduler = BackgroundScheduler()


def _run_scrape():
    from routes.scraper import do_scrape
    do_scrape()


def create_app():
    app = Flask(__name__, static_folder=None)
    app.secret_key = SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(scraper_bp)

    @app.route("/")
    def index():
        return send_from_directory(_frontend_dir, "index.html")

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory(os.path.join(_frontend_dir, "static"), filename)

    @app.route("/<path:path>")
    def frontend_routes(path):
        if path.endswith(".html") and os.path.isfile(os.path.join(_frontend_dir, path)):
            return send_from_directory(_frontend_dir, path)
        if os.path.isfile(os.path.join(_frontend_dir, "static", path)):
            return send_from_directory(os.path.join(_frontend_dir, "static"), path)
        return send_from_directory(_frontend_dir, "index.html")

    init_db()
    logger.info("Database initialized")

    if not scheduler.running:
        scheduler.add_job(
            func=_run_scrape,
            trigger="interval",
            hours=SCRAPE_INTERVAL_HOURS,
            id="scrape_jobs",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("Scheduler started (every %s hours)", SCRAPE_INTERVAL_HOURS)

    return app


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)
