import os
import sys
import tempfile

import pytest

# Ensure backend/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import database as db_module


@pytest.fixture(autouse=True)
def setup_db():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_module.DATABASE_PATH = tmp.name
    tmp.close()
    db_module.init_db()
    yield
    os.unlink(tmp.name)


@pytest.fixture
def app():
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()
