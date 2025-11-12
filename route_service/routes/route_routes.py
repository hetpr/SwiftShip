from flask import Blueprint, request, jsonify
from models.route_repo import (
    init_db, list_routes, get_route, create_route, update_route, delete_route, load_graph_from_db
)
from utils.route_solver import dijkstra, transport_suggestion, reliability_score

route_bp = Blueprint("route", __name__)
init_db()

@route_bp.route("/routes", methods=["GET"])
def routes_index():
    rows = list_routes()
    data = [
        {"id": r[0], "source": r[1], "destination": r[2], "distance_km": r[3]}
        for r in rows
    ]
    return jsonify(data)

@route_bp.route("/routes/<int:route_id>", methods=["GET"])
def routes_get(route_id):
    r = get_route(route_id)
    if not r: return jsonify({"error": "not found"}), 404
    return jsonify({"id": r[0], "source": r[1], "destination": r[2], "distance_km": r[3]})

@route_bp.route("/routes", methods=["POST"])
def routes_create():
    data = request.get_json(force=True)
    src = data.get("source"); dst = data.get("destination"); dist = data.get("distance_km")
    if not src or not dst or dist is None:
        return jsonify({"error": "source, destination, distance_km required"}), 400
    rid = create_route(src, dst, int(dist))
    return jsonify({"id": rid}), 201

@route_bp.route("/routes/<int:route_id>", methods=["PUT"])
def routes_update(route_id):
    data = request.get_json(force=True)
    src = data.get("source"); dst = data.get("destination"); dist = data.get("distance_km")
    if not src or not dst or dist is None:
        return jsonify({"error": "source, destination, distance_km required"}), 400
    if not get_route(route_id): return jsonify({"error": "not found"}), 404
    update_route(route_id, src, dst, int(dist))
    return jsonify({"status": "ok"})

@route_bp.route("/routes/<int:route_id>", methods=["DELETE"])
def routes_delete(route_id):
    if not get_route(route_id): return jsonify({"error": "not found"}), 404
    delete_route(route_id)
    return jsonify({"status": "deleted"})

@route_bp.route("/optimal_route", methods=["GET"])
def optimal_route():
    source = (request.args.get("source") or "").title()
    destination = (request.args.get("destination") or "").title()
    if not source or not destination:
        return jsonify({"error": "source & destination required"}), 400

    graph = load_graph_from_db()
    path, distance = dijkstra(graph, source, destination)
    if not path:
        return jsonify({"error": "No known route between given cities."}), 400

    return jsonify({
        "source": source,
        "destination": destination,
        "best_route": path,
        "total_distance_km": distance,
        "recommended_transport": transport_suggestion(distance),
        "route_reliability": reliability_score(path)
    })