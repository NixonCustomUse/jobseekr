import json
import os
import tempfile
import pytest

import database as db_module
from app import create_app


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
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_register(client):
    resp = client.post("/api/auth/register", json={
        "email": "test@test.com",
        "password": "pass123",
        "name": "Test User",
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Test User"
    assert data["plan"] == "free"


def test_register_duplicate(client):
    client.post("/api/auth/register", json={
        "email": "dup@test.com", "password": "pass", "name": "Dup",
    })
    resp = client.post("/api/auth/register", json={
        "email": "dup@test.com", "password": "pass", "name": "Dup",
    })
    assert resp.status_code == 409


def test_login(client):
    client.post("/api/auth/register", json={
        "email": "login@test.com", "password": "pass", "name": "Login",
    })
    resp = client.post("/api/auth/login", json={
        "email": "login@test.com", "password": "pass",
    })
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Login"


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "email": "bad@test.com", "password": "pass", "name": "Bad",
    })
    resp = client.post("/api/auth/login", json={
        "email": "bad@test.com", "password": "wrong",
    })
    assert resp.status_code == 401


def test_get_profile_requires_auth(client):
    resp = client.get("/api/profile")
    assert resp.status_code == 401


def test_update_profile(client):
    client.post("/api/auth/register", json={
        "email": "prof@test.com", "password": "pass", "name": "Prof",
    })
    resp = client.put("/api/profile", json={
        "resume_text": "5 years F&B manager",
        "preferred_location": "Kuala Lumpur",
    })
    assert resp.status_code == 200

    resp = client.get("/api/profile")
    data = resp.get_json()
    assert data["resume_text"] == "5 years F&B manager"
    assert data["preferred_location"] == "Kuala Lumpur"


def test_list_jobs(client):
    resp = client.get("/api/jobs")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_apply_requires_auth(client):
    resp = client.post("/api/applications", json={"job_id": 1})
    assert resp.status_code == 401


def test_apply_full_flow(client):
    client.post("/api/auth/register", json={
        "email": "apply@test.com", "password": "pass", "name": "Apply",
    })
    client.put("/api/profile", json={
        "resume_text": "3 years waitstaff experience",
    })

    import database as db
    db.execute(
        "INSERT INTO jobs (platform_id, title, company, location, category, description) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        ["js001", "Waiter", "Restoran ABC", "KL", "餐饮", "Looking for waiter"],
    )

    resp = client.post("/api/applications", json={"job_id": 1})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["status"] == "pending"

    resp = client.get("/api/applications")
    apps = resp.get_json()
    assert len(apps) == 1
    assert apps[0]["job_id"] == 1
