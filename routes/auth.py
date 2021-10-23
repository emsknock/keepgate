from flask.helpers import url_for
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
            return redirect(url_for("index"))
        else:
            return render_template("sign_in.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        next_url = request.form["next"]
        if len(username) > 32 or len(password) > 32 or not users.check_signin(username, password):
            flash("invalid_credentials")
            return redirect(url_for("signin"))
        else:
            users.signin(username)
            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for("index"))

@app.route("/signout")
def signout():
    users.signout()
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("sign_up.html")
    else:
        username = request.form["username"]
        new_password = request.form["new-password"]
        confirm_password = request.form["confirm-password"]
        can_make_user = True
        if len(username) > 32 or len(new_password) > 32:
            flash("credentials_too_long")
        if len(username) < 1 or len(new_password) < 1:
            flash("empty_credentials")
            can_make_user = False
        if new_password != confirm_password:
            flash("password_nomatch")
            can_make_user = False
        if not users.is_username_free(username):
            flash("username_taken")
            can_make_user = False
        if not can_make_user:
            return redirect(url_for("signup"))
        users.new_user(username, new_password)
        users.signin(username)
        return redirect(url_for("index"))