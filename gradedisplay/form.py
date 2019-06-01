# Import flask forms from flask_wtf
from flask_wtf import FlaskForm
# Import the types of feilds that we want to have, a string, password, submit and boolean feild
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Also get some validators that check length and the data required one as well
from wtforms.validators import Length, DataRequired

# Create a new object that inherits the flaskform properties, we want to add our additional attributes that this object should have
class LoginForm(FlaskForm):  
    # We want a uername feild, we restrict the length and put in a placeholder
    username = StringField('Username', validators=[Length(min=6, max=6)], render_kw={"placeholder": "Enter your username"})
    # Same as the username feild, we want a passord feild in which we restrict the length and add a placeholder
    password = PasswordField('Password', validators=[Length(min=6, max=8)], render_kw={"placeholder": "Enter your password"})
    # Add a remember me feild
    remember = BooleanField('Remember Me')
    # Add a submit feild
    submit = SubmitField('Login')

