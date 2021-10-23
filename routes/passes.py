from flask.helpers import flash, url_for
from utils import events, users, passes
from app import app
from flask import (
    render_template,
    redirect,
    session,
    request,
    abort
)

@app.route("/pass/<pass_id>", methods=["GET", "POST"])
@users.checks_csrf
def valuepass(pass_id):
    valuepass = passes.get_pass(pass_id)
    event = events.get_event_info(valuepass.event_id)
    if not valuepass:
        return abort(404)
    if request.method == "GET":
        return render_template(
            "pass_display.html",
            valuepass=valuepass,
            event=event
        )
    else:
        if not events.assert_user_owns_event(event.id): return
        if len(request.form["extra-info"]) > 512:
            flash("too_long_info")
            redirect("event_passes")
        passes.update_pass_data(
            pass_id,
            request.form["extra-info"]
        )
        return redirect(url_for("event_passes", event_id=event.id))

@app.route("/pass/<pass_id>/transactions")
@users.requires_signin
def pass_transactions(pass_id):
    valuepass = passes.get_pass(pass_id)
    event = events.get_event_info(valuepass.event_id)
    if not events.assert_user_owns_event(event.id): return
    return render_template(
        "pass_transactions.html",
        valuepass=valuepass,
        transactions=passes.get_pass_transactions(pass_id)
    )

@app.route("/pass/<pass_id>/manage")
@users.requires_signin
def pass_management(pass_id):
    valuepass = passes.get_pass(pass_id)
    event = events.get_event_info(valuepass.event_id)
    if not valuepass:
        return abort(404)
    return render_template(
        "pass_management.html",
        valuepass=valuepass,
        event=event
    )

@app.route("/pass/<pass_id>/value", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def pass_value(pass_id):
    
    valuepass = passes.get_pass(pass_id)
    if not valuepass:
        return abort(404)
    event = events.get_event_info(valuepass.event_id)

    if request.method == "GET":
        return str(valuepass.value);
    else:
        if not events.assert_user_owns_event(event.id): return # TODO: Check for organiser, not owner
        return str(passes.pass_modify_value(pass_id, int(request.form["value-delta"]), session["user_id"]))

