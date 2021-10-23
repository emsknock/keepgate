from app import app
from utils import events, organisers, users, passes

from flask import (
    render_template,
    redirect,
    session,
    request,
    abort,
    flash,
    url_for
)

@app.route("/pass/<pass_id>", methods=["GET", "POST", "DELETE"])
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
    if request.method == "POST":
        if not events.assert_user_owns_event(event.id): return
        if len(request.form["extra-info"]) > 512:
            flash("too_long_info")
            redirect("event_passes")
        passes.update_pass_data(
            pass_id,
            request.form["extra-info"]
        )
        return redirect(url_for("event_passes", event_id=event.id))
    if request.method == "DELETE":
        if not events.assert_user_owns_event(event.id): return abort(401)
        passes.delete_pass(pass_id)
        return "", 200

@app.route("/pass/<pass_id>/transactions")
@users.requires_signin
def pass_transactions(pass_id):
    valuepass = passes.get_pass(pass_id)
    if not valuepass: return abort(404)
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
    if not valuepass: return abort(404)
    event = events.get_event_info(valuepass.event_id)
    permissions = organisers.get_permissions(event.id)
    if not valuepass:
        return abort(404)
    if not permissions["can_topup"] and not permissions["can_deduct"]:
        flash("no_permissions")
        return redirect(url_for("index"))
    return render_template(
        "pass_management.html",
        valuepass=valuepass,
        event=event,
        permissions=permissions
    )

@app.route("/pass/<pass_id>/value", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def pass_value(pass_id):
    
    valuepass = passes.get_pass(pass_id)
    if not valuepass: return abort(404)

    if request.method == "GET":
        return str(valuepass.value);

    event = events.get_event_info(valuepass.event_id)
    permissions = organisers.get_permissions(event.id)
    if not permissions:
        flash("no_permissions")
        return redirect(url_for("index"))

    try:
        delta = int(request.form["value-delta"])
        if (delta > 0 and not permissions["can_topup"]) or (delta < 0 and not permissions["can_deduct"]):
            flash("no_permissions")
            return redirect(url_for("index"))
        newValue = passes.pass_modify_value(pass_id,
                                            delta,
                                            session["user_id"])
        return str(newValue)
    except ValueError:
        return abort(400)