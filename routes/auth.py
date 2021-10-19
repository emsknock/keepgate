from utils import users
from app import app
from flask import (
    render_template,
    redirect,
    request,
    flash
)

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