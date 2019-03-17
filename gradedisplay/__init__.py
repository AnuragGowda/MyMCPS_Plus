from flask import Flask
from flask_session import Session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

from gradedisplay import routes
