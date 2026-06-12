from flask import Blueprint, request, session, jsonify

from database import query, query_one, execute
from agent.resume_tailor import ResumeTailor
from agent.cover_letter import CoverLetterGenerator

applications_bp = Blueprint("applications", __name__)
tailor = ResumeTailor()
cover_gen = CoverLetterGenerator()


@applications_bp.route("/api/applications", methods=["GET"])
def list_applications():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    apps = query(
        """SELECT a.*, j.title, j.company, j.location, j.url
           FROM applications a
           JOIN jobs j ON a.job_id = j.id
           WHERE a.user_id = ?
           ORDER BY a.applied_at DESC""",
        [user_id],
    )
    return jsonify(apps)


@applications_bp.route("/api/applications", methods=["POST"])
def apply():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    data = request.get_json()
    job_id = data.get("job_id")
    if not job_id:
        return jsonify({"error": "job_id required"}), 400

    existing = query_one(
        "SELECT id FROM applications WHERE user_id = ? AND job_id = ?",
        [user_id, job_id],
    )
    if existing:
        return jsonify({"error": "already applied"}), 409

    job = query_one("SELECT * FROM jobs WHERE id = ?", [job_id])
    if not job:
        return jsonify({"error": "job not found"}), 404

    profile = query_one("SELECT * FROM profiles WHERE user_id = ?", [user_id])
    user = query_one("SELECT name FROM users WHERE id = ?", [user_id])

    resume_text = profile["resume_text"] if profile else ""
    user_name = user["name"] if user else ""

    custom_resume = tailor.tailor(resume_text, job) if resume_text else ""
    cover_letter = cover_gen.generate(user_name, resume_text, job) if resume_text else ""

    app_id = execute(
        """INSERT INTO applications (user_id, job_id, custom_resume, cover_letter)
           VALUES (?, ?, ?, ?)""",
        [user_id, job_id, custom_resume, cover_letter],
    )

    return jsonify({"id": app_id, "status": "pending"}), 201
