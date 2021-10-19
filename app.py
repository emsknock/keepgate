from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import app_routes
from routes import auth, event

if __name__ == "__main__":
    app.run(debug=True)