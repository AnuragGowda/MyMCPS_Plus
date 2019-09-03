# This is the initiation file that creates our module, here we configure our application
# Import flask
from flask import Flask
# Import sessions
from flask_session import Session
# Import the os module
from os import urandom
# Import CSRF protection
from flask_wtf.csrf import CSRFProtect
# Import crypto stuff to keep the secret key hidden, I did this with the email password too
import platform
import os, base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# Create the flask app
app = Flask(__name__)

# Do crypto stuff to make the user not know what the secret key is
cmpString = os.getcwd()+platform.platform()
key = base64.urlsafe_b64encode(cmpString[:32].encode('utf-8'))
f = Fernet(key)
password = f.encrypt(b'Let\'s make a really cool secret key!').decode('UTF-8')

# Configure the secret key, which is needed for the application
app.config['SECRET_KEY'] = password
# Set the session type to filesystem because the default system won't work for our purposes
app.config['SESSION_TYPE'] = 'filesystem'
# Active sessions for the app
Session(app)
# Activate csrf protection
csrf = CSRFProtect(app)

# Import the routes here 
from gradedisplay import routes
