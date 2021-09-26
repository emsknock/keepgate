from app import app
from flask import render_template

import db

@app.route("/")
def index():
    return render_template(
        "logged_in.html",
        username="Test",
        events=db.get_events(2)
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    return ""

@app.route("/logout")
def logout():
    return ""

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