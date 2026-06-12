from flask import Blueprint, request, jsonify

from database import query, query_one
from agent.matcher import JobMatcher

jobs_bp = Blueprint("jobs", __name__)
matcher = JobMatcher()


@jobs_bp.route("/api/jobs", methods=["GET"])
def list_jobs():
    category = request.args.get("category", "")
    location = request.args.get("location", "")
    keyword = request.args.get("keyword", "")

    sql = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if category:
        sql += " AND category = ?"
        params.append(category)
    if location:
        sql += " AND location LIKE ?"
        params.append(f"%{location}%")
    if keyword:
        sql += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
        kw = f"%{keyword}%"
        params.extend([kw, kw, kw])

    sql += " ORDER BY scraped_at DESC LIMIT 50"
    jobs = query(sql, params)
    return jsonify(jobs)


@jobs_bp.route("/api/jobs/<int:job_id>", methods=["GET"])
def job_detail(job_id):
    job = query_one("SELECT * FROM jobs WHERE id = ?", [job_id])
    if not job:
        return jsonify({"error": "job not found"}), 404
    return jsonify(job)


@jobs_bp.route("/api/jobs/<int:job_id>/match", methods=["POST"])
def match_job(job_id):
    from flask import session

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    job = query_one("SELECT * FROM jobs WHERE id = ?", [job_id])
    if not job:
        return jsonify({"error": "job not found"}), 404

    profile = query_one("SELECT * FROM profiles WHERE user_id = ?", [user_id])
    if not profile:
        return jsonify({"error": "profile not found"}), 404

    result = matcher.match_score(
        profile["resume_text"], profile["skills"], job
    )
    return jsonify(result)
