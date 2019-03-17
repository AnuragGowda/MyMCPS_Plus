from flask import Flask
from flask_session import Session
from flask_sslify import SSLify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
SSLify(app)

from gradedisplay import routes
