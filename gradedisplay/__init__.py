# This is the initiation file that creates our module, here we configure our application
# Import flask
from flask import Flask
# Import sessions
from flask_session import Session
# Import SSL connections
from flask_sslify import SSLify
# Import the os module
from os import urandom
# Import CSRF protection
from flask_wtf.csrf import CSRFProtect


# Create the flask app
app = Flask(__name__)
# Configure the secret key, which is needed for the application
app.config['SECRET_KEY'] = 'asdofhasi0dhfoispafiowneafoiw[dfb'
# Set the session type to filesystem because the default system won't work for our purposes
app.config['SESSION_TYPE'] = 'filesystem'
# Active sessions for the app
Session(app)
# Same with SSL connections, this also tries to force an SSL connection
#SSLify(app)
# Activate csrf protection
csrf = CSRFProtect(app)

# Import the routes here 
from gradedisplay import routes
