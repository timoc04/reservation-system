from flask import Blueprint, render_template, session

from .auth import login_required

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
    return render_template(
        "dashboard.html",
        user=session.get("user")
    )