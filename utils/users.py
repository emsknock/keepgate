from db import exec, commit
from werkzeug.security import check_password_hash, generate_password_hash

def new_user(username, password):
    exec(
        "INSERT INTO users (username, passhash) VALUES (:username, :passhash)",
        {
            "username": username,
            "passhash": generate_password_hash(password)
        }
    )
    commit()

def check_login(username, password):
    result = exec(
        "SELECT id, password FROM users WHERE username=:username",
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