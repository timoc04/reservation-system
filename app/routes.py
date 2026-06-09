from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from .auth import login_required, admin_required
from .database import create_reservation as db_create_reservation
from .database import get_all_reservations

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template(
        "index.html",
        user=session.get("user")
    )


@main.route("/dashboard")
@login_required
def dashboard():
    reservations = get_all_reservations()

    return render_template(
        "dashboard.html",
        user=session.get("user"),
        reservations=reservations
    )


@main.route("/reservations")
@login_required
def view_reservations():
    reservations = get_all_reservations()

    return render_template(
        "reservations.html",
        user=session.get("user"),
        reservations=reservations
    )


@main.route("/reservations/create", methods=["GET", "POST"])
@login_required
def create_reservation():
    if request.method == "POST":
        guest_name = request.form.get("guest_name", "").strip()
        accommodation = request.form.get("accommodation", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()

        if not guest_name or not accommodation or not start_date or not end_date:
            flash("All fields are required.", "error")
            return redirect(url_for("main.create_reservation"))

        if start_date > end_date:
            flash("The start date cannot be later than the end date.", "error")
            return redirect(url_for("main.create_reservation"))

        user = session.get("user")

        db_create_reservation(
            guest_name=guest_name,
            accommodation=accommodation,
            start_date=start_date,
            end_date=end_date,
            created_by=user.get("email")
        )

        flash("Reservation created successfully.", "success")
        return redirect(url_for("main.view_reservations"))

    return render_template(
        "create_reservation.html",
        user=session.get("user")
    )


@main.route("/admin/reservations")
@admin_required
def admin_reservations():
    reservations = get_all_reservations()

    return render_template(
        "admin_reservations.html",
        user=session.get("user"),
        reservations=reservations
    )