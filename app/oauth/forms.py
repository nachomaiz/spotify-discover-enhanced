from flask_wtf import FlaskForm
from wtforms import SubmitField

class LoginForm(FlaskForm):
    """Generate login button."""
    submit = SubmitField('Sign in to Spotify')

class LogoutForm(FlaskForm):
    """Generate logout button."""
    submit = SubmitField('Log out')

def get_login_form(authorized:bool):
    """Return logout form if authorized and login form if not."""
    if authorized:
        return LogoutForm()
    return LoginForm()
