from flask import Blueprint, render_template, request, redirect
from services.eta_admin_client import get_eta_history, add_eta_history, delete_eta_history

eta_history_bp = Blueprint("admin_eta", __name__)

@eta_history_bp.route("/admin/eta-history")
def history_list():
    history = get_eta_history()
    return render_template("admin_eta_history.html", history=history)

@eta_history_bp.route("/admin/eta-history/add", methods=["GET", "POST"])
def history_add():
    if request.method == "POST":
        add_eta_history(
            request.form["distance"],
            request.form["days"],
            request.form["priority"],
            request.form.get("notes", "")
        )
        return redirect("/admin/eta-history")

    return render_template("admin_eta_add.html")

@eta_history_bp.route("/admin/eta-history/delete/<int:hid>")
def history_delete(hid):
    delete_eta_history(hid)
    return redirect("/admin/eta-history")