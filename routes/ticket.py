from app import app
from utils import organisers, tickets, events, users

from flask import (
    render_template,
    redirect,
    session,
    request,
    abort,
    flash,
    url_for
)

@app.route("/ticket/<ticket_id>", methods=["GET", "POST", "DELETE"])
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
    if request.method == "POST":
        if not events.assert_user_owns_event(event.id): return
        if len(request.form["extra-info"]) > 512:
            flash("too_long_info")
            return redirect(url_for("event_tickets", event.id))
        tickets.update_ticket_data(
            ticket_id,
            request.form["extra-info"]
        )
        return redirect(url_for("event_tickets", event.id))
    if request.method == "DELETE":
        if not events.assert_user_owns_event(event.id): return abort(401)
        tickets.delete_ticket(ticket_id)
        return "", 200

@app.route("/ticket/<ticket_id>/check")
@users.requires_signin
def ticket_check(ticket_id):
    ticket = tickets.get_ticket(ticket_id)
    if not ticket: return abort(404)
    event = events.get_event_info(ticket.event_id)
    permissions = organisers.get_permissions(event.id)
    if not permissions or not permissions.can_stamp:
        flash("no_permissions")
        return redirect(url_for("index"))
    tickets.stamp_ticket(ticket_id, session["user_id"])
    return render_template(
        "ticket_check.html",
        ticket=ticket,
        event=event
    )

