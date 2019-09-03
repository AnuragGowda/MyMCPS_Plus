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
password = f.decrypt(b'gAAAAABdbuMhle4I0kvnQsW3e_TiLxY6ZNb2Ni4s7Eefl-TO9jVWPrQiCdWOSf-V7Lp9MBTjU9VvvufgWqb2K3V2WB3vOZ_UavPsC4Y_wZ9emQSiuodptuUB5asW995PB-u96Yt0V6fW').decode('UTF-8')

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
