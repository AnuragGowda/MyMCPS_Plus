# Import the app object from the gradedisplay package
from gradedisplay import app

# If running this file, run the app with this machine being the host and with debug mode turned off
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
