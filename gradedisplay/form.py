# Import flask forms from flask_wtf
from flask_wtf import FlaskForm
# Import the types of feilds that we want to have, a string, password, submit and boolean feild
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# Also get some validators that check length
from wtforms.validators import Length

# Create a new object that inherits the flaskform properties, we want to add our additional attributes that this object should have
class LoginForm(FlaskForm):  
    # We want a uername feild, we restrict the length and put in a placeholder
    username = StringField('Username', validators=[Length(min=6, max=6)], render_kw={"placeholder": "Enter your username"})
    # Same as the username feild, we want a passord feild in which we restrict the length and add a placeholder
    password = PasswordField('Password', validators=[Length(min=6, max=8)], render_kw={"placeholder": "Enter your password"})
    # Add a submit feild
    submit = SubmitField('Login')

# Create a new object that also inherits the flaskform properties, add more attributes
class ErrorForm(FlaskForm):
    # We need a string for the user's name
    name = StringField('Name (if you wish to be contacted)', validators=[Length(max=20)], render_kw={"placeholder": "Enter your name"})
    # We need an email feild for the users email
    email = StringField('Email (if you wish to be contacted)', validators=[Length(max=40)], render_kw={"placeholder": "Enter your email", "rows":20, "cols":20})
    # Text box in which the user can tell us what went wrong
    textbox = TextAreaField('Please describe what occured that led to this problem to the best of your ability.', validators=[Length(max=1000)], render_kw={"placeholder": "Click here to begin typing"})
    # Finally, we add a check box that the user clicks if they are ok with us seeing their grade data 
    info = BooleanField('Send Additional Info')
    # And, we also have a sumbit feild
    submit = SubmitField('Send Report')

