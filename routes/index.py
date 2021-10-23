from app import app
from utils import events, users

from flask import (
    render_template,
    session,
)

@app.route("/")
def index():
    if users.is_signed_in():
        return render_template(
            "index_signed_in.html",
            username=session["username"],
            own_events=events.get_detailed_event_list(session["user_id"])
        )
    else:
        return render_template("index.html")