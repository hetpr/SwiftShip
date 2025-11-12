from flask import Blueprint, render_template, request, redirect, session
from functools import wraps
from models.shipment_model import (
    add_shipment,
    get_all_shipments,
    get_shipment_by_id,
    update_shipment,
    delete_shipment,
    add_user,
    get_user
)
from services.eta_client import get_eta
from services.route_client import get_best_route

booking_bp = Blueprint("booking", __name__)

def login_required(f):
    @wraps(f)
    def protected(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return protected

@booking_bp.route("/")
def home():
    if "user_id" in session:
        return redirect("/book")
    return redirect("/login")

@booking_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        add_user(name, email, password)
        return redirect("/login")

    return render_template("signup.html")

@booking_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email, password)

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect("/book")
        else:
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

@booking_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@booking_bp.route("/book", methods=["GET"])
@login_required
def book_form():
    return render_template("create_shipment.html")

@booking_bp.route("/book", methods=["POST"])
@login_required
def book_shipment():
    sender = request.form["sender"]
    receiver = request.form["receiver"]
    source = request.form["source"]
    destination = request.form["destination"]
    weight = request.form["weight"]
    priority = request.form["priority"]

    best_route, distance = get_best_route(source, destination)

    route_str = " → ".join(best_route) if best_route else "Route not available"

    eta = get_eta(distance, priority)

    add_shipment(sender, receiver, source, destination, weight, eta)

    return render_template("booking_success.html",
                           sender=sender,
                           receiver=receiver,
                           source=source,
                           destination=destination,
                           weight=weight,
                           eta=eta,
                           priority=priority,
                           route=route_str,
                           distance=distance)

@booking_bp.route("/shipments")
@login_required
def shipments_list():
    shipments = get_all_shipments()
    return render_template("shipments_list.html", shipments=shipments)

@booking_bp.route("/edit/<int:shipment_id>", methods=["GET", "POST"])
@login_required
def edit_shipment(shipment_id):
    shipment = get_shipment_by_id(shipment_id)

    if request.method == "POST":
        sender = request.form["sender"]
        receiver = request.form["receiver"]
        source = request.form["source"]
        destination = request.form["destination"]
        weight = request.form["weight"]

        update_shipment(shipment_id, sender, receiver, source, destination, weight)
        return redirect("/shipments")

    return render_template("edit_shipment.html", shipment=shipment)

@booking_bp.route("/delete/<int:shipment_id>")
@login_required
def delete(shipment_id):
    delete_shipment(shipment_id)
    return redirect("/shipments")