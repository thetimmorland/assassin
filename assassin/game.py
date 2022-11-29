from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .db import get_db, queries

bp = Blueprint("game", __name__, url_prefix="/")


@bp.route("/", methods=("GET", "POST"))
def home():
    if g.user_id is None:
        flash("You must login to view that page.")
        return redirect(url_for("auth.login"))

    db = get_db()

    if request.method == "POST":
        kind = request.form.get("kind")

        if kind == "record_assassination":
            queries.create_assassination(db, prey_id=g.user_id)
            db.commit()
            flash("Assassination recorded.")

        elif kind == "set_is_active":
            is_active = request.form.get(
                "is_active", type=lambda v: v.lower() == "true"
            )
            queries.set_user_is_active(db, id=g.user_id, is_active=is_active)
            db.commit()
            flash(f"Participation {'resumed' if is_active else 'paused'}.")

        return redirect(url_for(".home"))

    data = queries.get_home_data(get_db(), id=g.user_id)
    return render_template("home.html", **data)


@bp.get("/leaderboard")
def leaderboard():
    data = queries.get_leaderboard_data(get_db())
    return render_template("leaderboard.html", data=data)
