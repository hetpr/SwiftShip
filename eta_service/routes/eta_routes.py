from flask import Blueprint, request, jsonify
from utils.eta_calculator import calculate_eta
from models.history_repo import (
    init_db, list_history, get_history, create_history, update_history, delete_history
)

eta_bp = Blueprint("eta", __name__)
init_db()

@eta_bp.route("/predict_eta", methods=["GET"])
def predict_eta():
    distance = request.args.get("distance", type=float)
    priority = request.args.get("priority", default="standard")
    if distance is None:
        return jsonify({"error": "distance parameter required"}), 400

    eta_str, total_days, applied = calculate_eta(distance, priority)
    return jsonify({
        "eta": eta_str,
        "days": total_days,
        "priority": applied["priority"],
        "adjustments": {
            "weather_delay_days": applied["weather_delay_days"],
            "weekend_pushed": applied["weekend_pushed"]
        }
    })

@eta_bp.route("/history", methods=["GET"])
def history_index():
    rows = list_history()
    data = [
        {
            "id": r[0],
            "distance_km": r[1],
            "actual_days": r[2],
            "priority": r[3],
            "notes": r[4],
            "created_at": r[5]
        } for r in rows
    ]
    return jsonify(data)

@eta_bp.route("/history/<int:hid>", methods=["GET"])
def history_get(hid):
    r = get_history(hid)
    if not r: return jsonify({"error": "not found"}), 404
    return jsonify({
        "id": r[0],
        "distance_km": r[1],
        "actual_days": r[2],
        "priority": r[3],
        "notes": r[4],
        "created_at": r[5]
    })

@eta_bp.route("/history", methods=["POST"])
def history_create():
    data = request.get_json(force=True)
    distance = data.get("distance_km")
    actual_days = data.get("actual_days")
    priority = data.get("priority")
    notes = data.get("notes")

    if distance is None or actual_days is None or priority not in ("standard","express","overnight"):
        return jsonify({"error": "distance_km, actual_days, priority ('standard'|'express'|'overnight') required"}), 400

    rid = create_history(distance, actual_days, priority, notes)
    return jsonify({"id": rid}), 201

@eta_bp.route("/history/<int:hid>", methods=["PUT"])
def history_update(hid):
    if not get_history(hid): return jsonify({"error": "not found"}), 404
    data = request.get_json(force=True)
    distance = data.get("distance_km")
    actual_days = data.get("actual_days")
    priority = data.get("priority")
    notes = data.get("notes")

    if distance is None or actual_days is None or priority not in ("standard","express","overnight"):
        return jsonify({"error": "distance_km, actual_days, priority ('standard'|'express'|'overnight') required"}), 400

    update_history(hid, distance, actual_days, priority, notes)
    return jsonify({"status": "ok"})

@eta_bp.route("/history/<int:hid>", methods=["DELETE"])
def history_delete(hid):
    if not get_history(hid): return jsonify({"error": "not found"}), 404
    delete_history(hid)
    return jsonify({"status": "deleted"})