import msal
from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .db import get_db, queries


def get_msal_app():
    return msal.ConfidentialClientApplication(
        client_id=current_app.config.get("AUTH_CLIENT_ID"),
        client_credential=current_app.config.get("AUTH_CLIENT_SECRET"),
    )


def initate_auth_code_flow():
    return get_msal_app().initiate_auth_code_flow(
        [], redirect_uri=url_for(".authorized", _external=True)
    )


def acquire_token_by_auth_code_flow():
    flow = session.get("flow", {})
    return get_msal_app().acquire_token_by_auth_code_flow(flow, request.args)


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_user_id():
    user_id = session.get("user_id")
    user = queries.get_user(get_db(), user_id)
    if user is not None:
        g.user_id = user["id"]
    else:
        g.user_id = None


@bp.get("/login")
def login():
    flow = initate_auth_code_flow()
    session["flow"] = flow
    return render_template(
        "login.html",
        login_url=flow["auth_uri"],
        signup_url=current_app.config.get("SIGNUP_URL"),
    )


@bp.get("/redirect")
def authorized():
    token = acquire_token_by_auth_code_flow()

    def error(msg):
        flash(msg)
        return redirect(url_for(".login"))

    if "error" in token:
        return error("Login failed. Unable to acquire token.")

    email = token.get("id_token_claims", {}).get("preferred_username")
    if email is None:
        return error("Login failed. Acquired token did not contain an email.")

    user = queries.get_user_by_email(get_db(), email)

    if user is None:
        return error(f'Login failed. Unable to find user with email "{email}".')

    session["user_id"] = user["id"]
    flash("Login successful.")
    return redirect(url_for("game.home"))


@bp.get("/logout")
def logout():
    session.clear()
    flash("Logout successful.")
    return redirect(url_for(".login"))
