from flask import Blueprint, request, session, jsonify

from database import query_one, execute

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/api/profile", methods=["GET"])
def get_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    profile = query_one(
        """SELECT u.name, u.email, u.phone, u.plan,
                  p.resume_text, p.skills,
                  p.preferred_location, p.preferred_category
           FROM users u
           LEFT JOIN profiles p ON u.id = p.user_id
           WHERE u.id = ?""",
        [user_id],
    )
    return jsonify(profile or {})


@profile_bp.route("/api/profile", methods=["PUT"])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    data = request.get_json()
    allowed = {"resume_text", "skills", "preferred_location", "preferred_category",
               "name", "phone"}

    if "name" in data or "phone" in data:
        updates = []
        params = []
        for field in ("name", "phone"):
            if field in data:
                updates.append(f"{field} = ?")
                params.append(data[field])
        if updates:
            params.append(user_id)
            execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)

    profile_fields = {k: v for k, v in data.items() if k in allowed
                      and k not in ("name", "phone")}
    if profile_fields:
        sets = []
        pparams = []
        for key, val in profile_fields.items():
            sets.append(f"{key} = ?")
            pparams.append(val if key != "skills" else str(val))
        pparams.append(user_id)
        execute(
            f"UPDATE profiles SET {', '.join(sets)} WHERE user_id = ?",
            pparams,
        )

    return jsonify({"ok": True})
