from flask_wtf import FlaskForm
from wtforms import SubmitField

class LoginForm(FlaskForm):
    submit = SubmitField('Sign in to Spotify')

class LogoutForm(FlaskForm):
    submit = SubmitField('Log out')

def get_login_form(authorized:bool):
    if authorized:
        return LogoutForm()
    return LoginForm()
