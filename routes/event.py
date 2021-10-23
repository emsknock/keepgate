from flask.helpers import url_for
from utils import events, users, tickets, passes, organisers
from app import app
from sqlalchemy.exc import IntegrityError
from flask import (
    render_template,
    redirect,
    request,
    session,
    flash
)

@app.route("/event/<event_id>/tickets", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def event_tickets(event_id):
    if not events.assert_user_owns_event(event_id): return
    if request.method == "GET":
        return render_template(
            "event_tickets.html",
            event=events.get_event_info(event_id),
            tickets=events.get_ticket_list(event_id)
        )
    else:
        tickets.new_tickets(event_id, int(request.form["new-ticket-count"]))
        return redirect(url_for("event_tickets", event_id=event_id))

@app.route("/event/<event_id>/passes", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def event_passes(event_id):
    if not events.assert_user_owns_event(event_id): return
    if request.method == "GET":
        return render_template(
            "event_passes.html",
            event=events.get_event_info(event_id),
            passes=events.get_pass_list(event_id)
        )
    else:
        passes.new_passes(event_id, int(request.form["new-pass-count"]))
        return redirect(url_for("event_passes", event_id=event_id))

@app.route("/event/<event_id>/organisers", methods=["GET", "POST"])
@users.requires_signin
def event_organisers(event_id):
    if not events.assert_user_owns_event(event_id): return
    if request.method == "GET":
        return render_template(
            "event_organisers.html",
            event=events.get_event_info(event_id),
            organisers=events.get_organiser_list(event_id)
        )
    else:
        new_organiser_id = users.get_id_by_username(request.form["new-organiser-username"])
        can_add_organiser = True
        if not new_organiser_id:
            flash("no_such_user")
            can_add_organiser = False
        if new_organiser_id == session["user_id"]:
            flash("refers_to_self")
            can_add_organiser = False
        if can_add_organiser:
            try:
                organisers.add_organiser(event_id, new_organiser_id)
            except IntegrityError:
                flash("already_added")
        return redirect(url_for("event_organisers", event_id=event_id))

@app.route("/event/<event_id>", methods=["POST"])
@users.requires_signin
@users.checks_csrf
def event(event_id):
    if not events.assert_user_owns_event(event_id): return
    events.update_event_data(
        event_id,
        request.form["title"],
        request.form["extra-info"],
        request.form["date"]
    )
    return redirect(url_for("event_tickets", event_id=event_id))

@app.route("/event", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def new_event():
    if request.method == "GET":
        return render_template("event_new.html")
    else:
        event_id = events.new_event(
            session["user_id"],
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )
        return redirect(url_for("event_tickets", event_id=event_id))