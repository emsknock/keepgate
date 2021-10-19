from utils import events, users
from app import app
from flask import (
    render_template,
    redirect,
    request,
    session,
    flash
)

@app.route("/event/<id>", methods=["GET", "POST"])
@users.requires_signin
def event(id):
    if not events.does_user_own_event(session["user_id"], id):
        flash("not_own_event")
        return redirect("/")
    if request.method == "GET":
        return render_template(
            "event.html",
            event=events.get_event_info(id)
        )
    else:
        events.update_event_data(
            id,
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )
        return redirect("/")

@app.route("/event", methods=["GET", "POST"])
@users.requires_signin
def new_event():
    if request.method == "GET":
        return render_template("new_event.html")
    else:
        event_id = events.new_event(
            session["user_id"],
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )
        return redirect(f"/event/{event_id}")