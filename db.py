from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
connection = SQLAlchemy(app)

def done():
    connection.session.execute()

def new_user(username, password):
    connection.session.execute(
        "INSERT INTO users (username, passhash) VALUES (:username, :passhash)",
        {
            "username": username,
            "passhash": generate_password_hash(password)
        }
    )
    done()

def check_user(username, password):
    result = connection.session.execute(
        "SELECT id, password FROM users WHERE username=:username",
        {
            "username": username
        }
    )
    user = result.fetchone()
    return (user is not None) and check_password_hash(user.passhash, password)

def new_ticket(event_id, ticketholder, extra_info):
    connection.session.execute(
        "INSERT INTO tickets (id, event_id, holder, extra_info) VALUES (:id, :event_id, :holder, :extra_info)",
        {
            "id": uuid.uuid4(),
            "event_id": event_id,
            "holder": ticketholder,
            "extra_info": extra_info
        }
    )
    done()