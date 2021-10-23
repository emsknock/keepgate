from flask.helpers import url_for
from utils import tickets, events, users
from app import app
from flask import (
    render_template,
    redirect,
    session,
    request,
    abort
)

@app.route("/ticket/<ticket_id>", methods=["GET", "POST"])
@users.checks_csrf
def ticket(ticket_id):
    ticket = tickets.get_ticket(ticket_id)
    if not ticket: return abort(404)
    event = events.get_event_info(ticket.event_id)
    if request.method == "GET":
        return render_template(
            "ticket_display.html",
            ticket=ticket,
            event=event
        )
    else:
        if not events.assert_user_owns_event(event.id): return
        tickets.update_ticket_data(
            ticket_id,
            request.form["extra-info"]
        )
        return redirect(url_for("event_tickets", event.id))

@app.route("/ticket/<ticket_id>/check")
@users.requires_signin
def ticket_check(ticket_id):
    ticket = tickets.get_ticket(ticket_id)
    event = events.get_event_info(ticket.event_id)
    if not ticket:
        return abort(404)
    tickets.stamp_ticket(ticket_id, session["user_id"])
    return render_template(
        "ticket_check.html",
        ticket=ticket,
        event=event
    )

