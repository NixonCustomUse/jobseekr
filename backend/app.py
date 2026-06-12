import logging
from datetime import datetime

from flask import Flask

from config import SECRET_KEY, SCRAPE_INTERVAL_HOURS
from database import init_db
from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.profile import profile_bp
from routes.applications import applications_bp

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(applications_bp)

    init_db()
    logger.info("Database initialized")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
