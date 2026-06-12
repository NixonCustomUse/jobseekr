import hashlib
import os

from flask import Blueprint, request, session, jsonify

from database import query_one, execute

auth_bp = Blueprint("auth", __name__)


def _hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()
    h = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
    return f"{salt}:{h}"


def _check_password(password, stored):
    salt, h = stored.split(":", 1)
    return _hash_password(password, salt) == stored


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    name = data.get("name", "").strip()

    if not email or not password or not name:
        return jsonify({"error": "email, password, name required"}), 400

    existing = query_one("SELECT id FROM users WHERE email = ?", [email])
    if existing:
        return jsonify({"error": "email already registered"}), 409

    password_hash = _hash_password(password)
    user_id = execute(
        "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
        [email, password_hash, name],
    )
    execute(
        "INSERT INTO profiles (user_id, preferred_category) VALUES (?, '餐饮')",
        [user_id],
    )

    session["user_id"] = user_id
    session["name"] = name
    return jsonify({"id": user_id, "name": name, "plan": "free"}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    user = query_one("SELECT * FROM users WHERE email = ?", [email])
    if not user or not _check_password(password, user["password_hash"]):
        return jsonify({"error": "invalid email or password"}), 401

    session["user_id"] = user["id"]
    session["name"] = user["name"]
    return jsonify({"id": user["id"], "name": user["name"], "plan": user["plan"]})


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})
