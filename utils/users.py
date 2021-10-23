from db import exec, commit

from functools import wraps
from secrets import token_hex
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    redirect,
    request,
    session,
    abort,
    flash,
    url_for
)

def new_user(username, password):
    exec(
        "INSERT INTO users (username, passhash) VALUES (:username, :passhash)",
        {
            "username": username,
            "passhash": generate_password_hash(password)
        }
    )
    commit()

def get_id_by_username(username):
    result = exec(
        "SELECT id FROM users WHERE username=:username",
        {
            "username": username
        }
    )
    row = result.fetchone()
    return row.id if row else None

def check_signin(username, password):
    result = exec(
        "SELECT id, passhash FROM users WHERE username=:username",
        {
            "username": username
        }
    )
    user = result.fetchone()
    return user and check_password_hash(user.passhash, password)

def is_username_free(username):
    result = exec(
        "SELECT id FROM users WHERE username=:username",
        {
            "username": username
        }
    )
    user = result.fetchone()
    return not user

def requires_signin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session and session["username"] != "":
            return f(*args, **kwargs)
        else:
            flash("requires_signin")
            return redirect(url_for("signin", next=request.url))
    return decorated_function

def checks_csrf(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method != "POST" or request.form["csrf"] == session["csrf_token"]:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function


def is_signed_in(): return (
    "username" in session and
    "user_id" in session and
    session["username"] != "" and
    session["user_id"] != ""
)

def signin(username):
    session["username"] = username
    session["user_id"] = get_id_by_username(username)
    session["csrf_token"] = token_hex(16)

def signout():
    if "username" in session:
        del session["username"]
    if "user_id" in session:
        del session["user_id"]