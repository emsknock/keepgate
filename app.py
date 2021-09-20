#!/usr/bin/env python3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)

import routes

if __name__ == '__main__':
	app.run(debug=True)