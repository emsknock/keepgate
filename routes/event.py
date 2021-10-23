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

@app.route("/event/<id>/tickets", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def event_tickets(id):
    if not events.does_user_own_event(session["user_id"], id):
        flash("not_own_event")
        return redirect("/")
    if request.method == "GET":
        return render_template(
            "event_tickets.html",
            event=events.get_event_info(id),
            tickets=events.get_ticket_list(id)
        )
    else:
        tickets.new_tickets(id, int(request.form["new-ticket-count"]))
        return redirect("./tickets")

@app.route("/event/<id>/passes", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def event_passes(id):
    if not events.does_user_own_event(session["user_id"], id):
        flash("not_own_event")
        return redirect("/")
    if request.method == "GET":
        return render_template(
            "event_passes.html",
            event=events.get_event_info(id),
            passes=events.get_pass_list(id)
        )
    else:
        passes.new_passes(id, int(request.form["new-pass-count"]))
        return redirect("./passes")

@app.route("/event/<id>/organisers", methods=["GET", "POST"])
@users.requires_signin
def event_organisers(id):
    if not events.does_user_own_event(session["user_id"], id):
        flash("not_own_event")
        return redirect("/")
    if request.method == "GET":
        return render_template(
            "event_organisers.html",
            event=events.get_event_info(id),
            organisers=events.get_organiser_list(id)
        )
    else:
        new_organiser_id = users.get_id_by_username(request.form["new-organiser-username"])
        if not new_organiser_id:
            flash("no_such_user")
            return redirect("./organisers")
        if new_organiser_id == session["user_id"]:
            flash("refers_to_self")
            return redirect("./organisers")
        try:
            organisers.add_organiser(id, new_organiser_id)
        except IntegrityError:
            flash("already_added")
        return redirect("./organisers")

@app.route("/event/<id>", methods=["POST"])
@users.requires_signin
@users.checks_csrf
def event(id):
    if not events.does_user_own_event(session["user_id"], id):
        flash("not_own_event")
        return redirect("/")
    else:
        events.update_event_data(
            id,
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )
        return redirect(f"/event/{id}/tickets")

@app.route("/event", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def new_event():
    if request.method == "GET":
        return render_template("event_new.html")
    else:
        id = events.new_event(
            session["user_id"],
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )
        return redirect(f"/event/{id}/tickets")