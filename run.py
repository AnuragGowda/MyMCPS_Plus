# Import the app object from the gradedisplay package
from gradedisplay import app

# If running this file, we continue
if __name__ == '__main__':
    # The code that 'runs' the app, set the host to the machine it is running on, also turn off debug mode which is actually the default, so this is kind of unnecessary
    app.run(host='0.0.0.0', debug=False)
