from db import exec, commit
from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps
from flask import g, request, redirect, url_for, session

def requires_signin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session and session["username"] != "":
            return f(*args, **kwargs)
        else:
            return redirect("/")
    return decorated_function

def is_signed_in(session): return (
    "username" in session and
    "user_id" in session and
    session["username"] != "" and
    session["user_id"] != ""
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
    return result.fetchone()[0]

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

def signin(username, session):
    session["username"] = username
    session["user_id"] = get_id_by_username("username")

def signout(session):
    if "username" in session:
        del session["username"]
    if "user_id" in session:
        del session["user_id"]