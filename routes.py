from utils import events, users
from app import app
from flask import (
    render_template,
    redirect,
    request,
    session
)

@app.route("/")
def index():
    if "username" not in session or session["username"] == "":
        return render_template("index.html")
    else:
        return render_template(
            "index_logged_in.html",
            username=session["username"],
            own_events=events.get_detailed_event_list(session["user_id"])
        )

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        if "username" not in session or session["username"] == "":
            return render_template("signin.html")
        else:
            return redirect("/")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if users.check_signin(username, password):
            session["username"] = username
            session["user_id"] = users.get_id_by_username(username)
            return redirect("/")
        else:
            return "TODO" # TODO: Wrong username or password

@app.route("/signout")
def signout():
    del session["username"]
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        new_password = request.form["new-password"]
        confirm_password = request.form["confirm-password"]
        if new_password != confirm_password:
            return "TODO" # TODO: Passwords don't match
        if users.is_username_free(username):
            users.new_user(username, new_password)
            session["username"] = username
            session["user_id"] = users.get_id_by_username(username)
            return redirect("/")
        else:
            return "TODO" # TODO: Username taken

@app.route("/event/<id>", methods=["GET", "DELETE"])
def event():
    return ""

@app.route("/event", methods=["GET", "POST"])
@users.requires_signin
def new_event():
    if request.method == "GET":
        return render_template("new_event.html")
    else:
        events.new_event(
            session["user_id"],
            request.form["title"],
            request.form["extra-info"],
            request.form["date"]
        )

@app.route("/ticket/<id>", methods=["GET", "DELETE"])
def ticket():
    return ""

@app.route("/ticket", methods=["POST"])
def new_ticket():
    return ""