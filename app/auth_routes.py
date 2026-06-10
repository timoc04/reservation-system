from flask import Blueprint, redirect, request, session, url_for

from .auth import build_auth_url, build_msal_app
from .config import Config

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return redirect(build_auth_url())


@auth.route("/auth/callback")
def auth_callback():
    if "code" not in request.args:
        return "Authentication failed: no authorisation code was returned.", 401

    result = build_msal_app().acquire_token_by_authorization_code(
        code=request.args["code"],
        scopes=Config.ENTRA_SCOPE,
        redirect_uri=Config.REDIRECT_URI
    )

    if "id_token_claims" not in result:
        error_description = result.get("error_description", "No error description available.")
        return f"Authentication failed: {error_description}", 401

    claims = result["id_token_claims"]

    user_email = claims.get("preferred_username", "").lower()

    session["user"] = {
        "name": claims.get("name"),
        "email": user_email,
        "object_id": claims.get("oid"),
        "is_admin": user_email in Config.ADMIN_EMAILS
    }

    next_url = session.pop("next_url", url_for("main.dashboard"))
    return redirect(next_url)


@auth.route("/logout")
def logout():
    session.clear()

    logout_url = (
        f"https://login.microsoftonline.com/{Config.ENTRA_TENANT_ID}"
        "/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={url_for('main.index', _external=True)}"
    )

    return redirect(logout_url)