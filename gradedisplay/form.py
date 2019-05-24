from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired

class LoginForm(FlaskForm):  
    username = StringField('Username', validators=[Length(min=6, max=6)], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[Length(min=6, max=8)], render_kw={"placeholder": "Enter your password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

