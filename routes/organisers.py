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

@app.route("/organiser/<event_id>/<organiser_id>", methods=["POST", "DELETE"])
@users.checks_csrf
def organiser(event_id, organiser_id):
    if not events.assert_user_owns_event(event_id): return
    if request.method == "POST":
        organisers.update_organiser(
            organiser_id,
            can_create = bool(request.form.get("can-create")),
            can_delete = bool(request.form.get("can-delete")),
            can_stamp = bool(request.form.get("can-stamp")),
            can_unstamp = bool(request.form.get("can-unstamp")),
            can_topup = bool(request.form.get("can-topup")),
            can_deduct = bool(request.form.get("can-deduct"))
        )
        return redirect(url_for("event_organisers", event_id=event_id))
    if request.method == "DELETE":
        organisers.delete_organiser(event_id, organiser_id)
        return "", 200