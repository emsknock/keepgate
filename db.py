from app import app
from flask_sqlalchemy import SQLAlchemy
import os
import re

import uuid
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
connection = SQLAlchemy(app)

def commit():
    connection.session.commit()

def new_user(username, password):
    connection.session.execute(
        "INSERT INTO users (username, passhash) VALUES (:username, :passhash)",
        {
            "username": username,
            "passhash": generate_password_hash(password)
        }
    )
    commit()

def check_user(username, password):
    result = connection.session.execute(
        "SELECT id, password FROM users WHERE username=:username",
        {
            "username": username
        }
    )
    user = result.fetchone()
    return (user is not None) and check_password_hash(user.passhash, password)

def new_event(user_id, title, date):
    connection.session.execute(
        "INSERT INTO events (user_id, title, date) VALUES (:user, :title, :date)",
        {
            "user": "2",
            "title": "Test event",
            "date": "2021-09-21"
        }
    )

def get_events(user_id):
    result = connection.session.execute(
        "SELECT title, date FROM events e WHERE e.user_id = :user_id",
        {
            "user_id": user_id
        }
    )
    return result.fetchall()

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
    commit()

def get_tickets(user_id):
    result = connection.session.execute(
        "SELECT (event_id, holder) FROM tickets"
    )
    return result.fetchall()