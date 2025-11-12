from flask import Blueprint, render_template, request, redirect
from services.route_admin_client import (
    get_routes, add_route, get_route, update_route, delete_route
)

route_admin_bp = Blueprint("route_admin", __name__)

@route_admin_bp.route("/admin/routes")
def route_list():
    routes = get_routes()
    return render_template("admin_routes_list.html", routes=routes)

@route_admin_bp.route("/admin/routes/add", methods=["GET", "POST"])
def route_add_view():
    if request.method == "POST":
        add_route(request.form["source"], request.form["destination"], request.form["distance"])
        return redirect("/admin/routes")
    return render_template("admin_routes_add.html")

@route_admin_bp.route("/admin/routes/edit/<int:rid>", methods=["GET", "POST"])
def route_edit(rid):
    route = get_route(rid)

    if request.method == "POST":
        update_route(rid, request.form["source"], request.form["destination"], request.form["distance"])
        return redirect("/admin/routes")

    return render_template("admin_routes_edit.html", route=route)

@route_admin_bp.route("/admin/routes/delete/<int:rid>")
def route_delete_view(rid):
    delete_route(rid)
    return redirect("/admin/routes")