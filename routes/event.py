from utils import events, users, tickets, passes
from app import app
from flask import (
    render_template,
    redirect,
    request,
    session,
    flash
)

@app.route("/event/<id>/tickets", methods=["GET", "POST"])
@users.requires_signin
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
        print(request.form)
        tickets.new_tickets(id, int(request.form["new-ticket-count"]))
        return redirect("./tickets")

@app.route("/event/<id>/passes", methods=["GET", "POST"])
@users.requires_signin
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

@app.route("/event/<id>/organisers")
@users.requires_signin
def event_organisers(id):
    if not events.does_user_own_event(session["user_id"], id):
        flash("not_own_event")
        return redirect("/")
    return render_template(
        "event_organisers.html",
        event=events.get_event_info(id),
        organisers=events.get_organiser_list(id)
    )

@app.route("/event/<id>", methods=["POST"])
@users.requires_signin
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