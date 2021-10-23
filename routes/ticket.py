from utils import tickets, events, users
from app import app
from flask import (
    render_template,
    redirect,
    session,
    request,
    abort
)

@app.route("/ticket/<id>", methods=["GET", "POST"])
@users.checks_csrf
def ticket(id):
    ticket = tickets.get_ticket(id)
    event = events.get_event_info(ticket.event_id)
    if not ticket:
        return abort(404)
    if request.method == "GET":
        return render_template(
            "ticket_display.html",
            ticket=ticket,
            event=event
        )
    else:
        if not events.assert_user_owns_event(event.id): return
        tickets.update_ticket_data(
            id,
            request.form["extra-info"]
        )
        return redirect(f"/event/{event.id}/tickets")

@app.route("/ticket/<id>/check")
@users.requires_signin
def ticket_check(id):
    ticket = tickets.get_ticket(id)
    event = events.get_event_info(ticket.event_id)
    if not ticket:
        return abort(404)
    tickets.stamp_ticket(id, session["user_id"])
    return render_template(
        "ticket_check.html",
        ticket=ticket,
        event=event
    )

