from utils import users
from app import app
from flask import (
    render_template,
    redirect,
    request,
    session
)

from utils.users import *

@app.route("/")
def index():
    if "username" not in session or session["username"] == "":
        return render_template("index.html")
    else:
        return render_template(
            "index_logged_in.html",
            username=session["username"]
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
        password = request.form["pass"]
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
        password = request.form["password"]
        if is_username_free(username):
            new_user(username, password)
            session["username"] = username
            return redirect("/")
        else:
            return "TODO" # TODO: Username taken

@app.route("/event/<id>", methods=["GET", "DELETE"])
def event():
    return ""

@app.route("/event", methods=["POST"])
def new_event():
    return ""

@app.route("/ticket/<id>", methods=["GET", "DELETE"])
def ticket():
    return ""

@app.route("/ticket", methods=["POST"])
def new_ticket():
    return ""