from functools import wraps

import msal
from flask import redirect, request, session, url_for

from .config import Config


def build_msal_app():
    return msal.ConfidentialClientApplication(
        client_id=Config.ENTRA_CLIENT_ID,
        authority=Config.ENTRA_AUTHORITY,
        client_credential=Config.ENTRA_CLIENT_SECRET
    )


def build_auth_url():
    return build_msal_app().get_authorization_request_url(
        scopes=Config.ENTRA_SCOPE,
        redirect_uri=url_for("auth.auth_callback", _external=True)
    )


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            session["next_url"] = request.url
            return redirect(url_for("auth.login"))

        return route_function(*args, **kwargs)

    return wrapper