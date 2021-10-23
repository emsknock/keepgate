from app import app
from utils import events, tickets, users, passes

import re
from sqlalchemy.exc import IntegrityError
from flask import (
    render_template,
    redirect,
    request,
    session,
    flash,
    abort,
    url_for
)

@app.route("/event/<event_id>/tickets", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def event_tickets(event_id):
    if not events.assert_user_owns_event(event_id): return
    event = events.get_event_info(event_id)
    ticket = events.get_ticket_list(event_id)
    if not event:
        flash("no_such_event")
        return(url_for("index"))
    if request.method == "GET":
        return render_template(
            "event_tickets.html",
            event=event,
            tickets=ticket
        )
    else:
        try:
            ticket_count = int(request.form["new-ticket-count"])
            tickets.new_tickets(event_id, ticket_count)
            return redirect(url_for("event_tickets", event_id=event_id))
        except:
            return abort(400)

@app.route("/event/<event_id>/passes", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def event_passes(event_id):
    if not events.assert_user_owns_event(event_id): return
    event = events.get_event_info(event_id)
    passe = events.get_pass_list(event_id)
    if not event:
        flash("no_such_event")
        return(url_for("index"))
    if request.method == "GET":
        return render_template(
            "event_passes.html",
            event=event,
            passes=passe
        )
    else:
        try:
            pass_count = int(request.form["new-pass-count"])
            passes.new_passes(event_id, pass_count)
            return redirect(url_for("event_passes", event_id=event_id))
        except:
            return abort(400)

@app.route("/event/<event_id>/organisers", methods=["GET", "POST"])
@users.requires_signin
def event_organisers(event_id):
    if not events.assert_user_owns_event(event_id): return
    event = events.get_event_info(event_id)
    organisers = events.get_organiser_list(event_id)
    if not event:
        flash("no_such_event")
        return(url_for("index"))
    if request.method == "GET":
        return render_template(
            "event_organisers.html",
            event=event,
            organisers=organisers
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

@app.route("/event/<event_id>", methods=["POST", "DELETE"])
@users.requires_signin
@users.checks_csrf
def event(event_id):
    if not events.assert_user_owns_event(event_id): return
    if request.method == "DELETE":
        events.delete_event(event_id)
        return "", 200
    else:
        try:
            title = request.form["title"]
            extra_info = request.form["extra-info"]
            date = request.form["date"]
            can_make_event = True
            if len(title) < 1:
                flash("no_title")
                can_make_event = False
            if len(title) > 32:
                flash("too_long_title")
                can_make_event = False
            if len(extra_info) > 512:
                flash("too_long_info")
                can_make_event = False
            if date != "" and not re.match(r"\d{4}-(0[1-9]|1[0-2])-([0-2][1-9]|3[01])"):
                return abort(400)
            if not can_make_event:
                return redirect(request.referrer)
            events.update_event_data(
                event_id,
                title,
                extra_info,
                date
            )
        except:
            return abort(400)
        return redirect(url_for("event_tickets", event_id=event_id))

@app.route("/event", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def new_event():
    if request.method == "GET":
        return render_template("event_new.html")
    else:
        title = request.form["title"]
        extra_info = request.form["extra-info"]
        date = request.form["date"]
        can_make_event = True
        if len(title) < 1:
            flash("no_title")
            can_make_event = False
        if len(title) > 32:
            flash("too_long_title")
            can_make_event = False
        if len(extra_info) > 512:
            flash("too_long_info")
            can_make_event = False
        if date != "" and not re.match(r"\d{4}-(0[1-9]|1[0-2])-([0-2][1-9]|3[01])", date):
            return abort(400)
        if not can_make_event:
            return redirect(url_for("new_event"))
        event_id = events.new_event(
            session["user_id"],
            title,
            extra_info,
            date
        )
        return redirect(url_for("event_tickets", event_id=event_id))