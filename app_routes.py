from utils import events, users, tickets
from app import app
from flask import (
    render_template,
    session,
)

@app.route("/")
def index():
    if users.is_signed_in():
        return render_template(
            "index_logged_in.html",
            username=session["username"],
            own_events=events.get_detailed_event_list(session["user_id"])
        )
    else:
        return render_template("index.html")

@app.route("/ticket/<id>", methods=["GET", "DELETE"])
def ticket(id):
    return render_template(
        "ticket_display.html",
        event=events.get_event_info(3),
        ticket=tickets.get_ticket(id)
    )

@app.route("/ticket", methods=["POST"])
def new_ticket():
    return ""