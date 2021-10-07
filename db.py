from app import app
from flask_sqlalchemy import SQLAlchemy
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

def commit():
    db.session.commit()

def exec(*args, **kwargs):
    return db.session.execute(*args, **kwargs)