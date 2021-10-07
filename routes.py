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
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session["username"]:
            return redirect("/")
        else:
            return "TODO" # TODO: Login page
    else:
        username = request.form["username"]
        password = request.form["pass"]
        if users.check_login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return "TODO" # TODO: Wrong username or password

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return ""

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