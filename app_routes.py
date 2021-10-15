from utils import events, users, tickets
from app import app
from flask import (
    render_template,
    redirect,
    request,
    session,
    flash
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

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        if users.is_signed_in():
            return redirect("/")
        else:
            return render_template("signin.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if users.check_signin(username, password):
            users.signin(username)
            return redirect("/")
        else:
            flash("invalid_credentials")
            return redirect("/signin")

@app.route("/signout")
def signout():
    users.signout()
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        new_password = request.form["new-password"]
        confirm_password = request.form["confirm-password"]
        can_make_user = True
        if new_password != confirm_password:
            flash("password_nomatch")
            can_make_user = False
        if not users.is_username_free(username):
            flash("username_taken")
            can_make_user = False
        if not can_make_user:
            return redirect("/signup")
        users.new_user(username, new_password)
        users.signin(username)
        return redirect("/")

@app.route("/event/<id>", methods=["GET", "POST"])
@users.requires_signin
def event(id):
    if not events.does_user_own_event(session["user_id"], id):
        flash("not_own_event")
        return redirect("/")
    if request.method == "GET":
        return render_template(
            "event.html",
            event=events.get_event_info(id)
        )
    else:
        events.update_event_data(
            id,
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )
        return redirect("/")

@app.route("/event", methods=["GET", "POST"])
@users.requires_signin
def new_event():
    if request.method == "GET":
        return render_template("new_event.html")
    else:
        event_id = events.new_event(
            session["user_id"],
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )
        return redirect(f"/event/{event_id}")

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