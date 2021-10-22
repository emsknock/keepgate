from utils import tickets, events, users, passes
from app import app
from flask import (
    render_template,
    redirect,
    session,
    request,
    abort,
    flash
)

@app.route("/pass/<id>", methods=["GET", "POST"])
@users.checks_csrf
def valuepass(id):
    valuepass = passes.get_pass(id)
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
        if not events.does_user_own_event(session["user_id"], event.id):
            flash("not_own_event")
            return redirect("/")
        passes.update_pass_data(
            id,
            request.form["extra-info"]
        )
        return redirect(f"/event/{event.id}/tickets")

@app.route("/pass/<id>/transactions")
@users.requires_signin
def pass_transactions(id):
    valuepass = passes.get_pass(id)
    event = events.get_event_info(valuepass.event_id)
    if not events.does_user_own_event(session["user_id"], event.id):
        flash("not_own_event")
        redirect("/")
    return render_template(
        "pass_transactions.html",
        valuepass=valuepass,
        transactions=passes.get_pass_transactions(id)
    )

@app.route("/pass/<id>/manage")
@users.requires_signin
def pass_management(id):
    valuepass = passes.get_pass(id)
    event = events.get_event_info(valuepass.event_id)
    if not valuepass:
        return abort(404)
    return render_template(
        "pass_management.html",
        valuepass=valuepass,
        event=event
    )

@app.route("/pass/<id>/value", methods=["GET", "POST"])
@users.requires_signin
@users.checks_csrf
def pass_value(id):
    
    valuepass = passes.get_pass(id)
    if not valuepass:
        return abort(404)
    event = events.get_event_info(valuepass.event_id)

    if request.method == "GET":
        return str(valuepass.value);
    else:
        if not events.does_user_own_event(session["user_id"], event.id):
            flash("not_own_event")
            return redirect("/") # TODO Check for organiser, not owner
        return str(passes.pass_modify_value(id, int(request.form["value-delta"]), session["user_id"]))

