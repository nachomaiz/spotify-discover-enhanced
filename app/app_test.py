# pylint: disable = missing-function-docstring
# pylint: disable = missing-class-docstring
# pylint: disable = invalid-name

from flask import Flask, flash, redirect, url_for
from flask_dance.contrib.spotify import make_spotify_blueprint, spotify
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.exc import NoResultFound

import os
import credentials

## Config

basedir = os.path.abspath(os.path.dirname(__file__))


def register_environment_variables() -> None:
    """Register environment variables for Spotipy and Flask."""

    # Dev: NOSHIP
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Spotipy
    # os.environ["SPOTIPY_CLIENT_ID"] = credentials.SPOTIPY_CLIENT_ID
    # os.environ["SPOTIPY_CLIENT_SECRET"] = credentials.SPOTIPY_CLIENT_SECRET
    # os.environ["SPOTIPY_REDIRECT_URI"] = credentials.SPOTIPY_REDIRECT_URI

    # Flask
    os.environ["APP_SECRET_KEY"] = credentials.APP_SECRET_KEY
    os.environ["SPOTIFY_OAUTH_CLIENT_ID"] = credentials.SPOTIPY_CLIENT_ID
    os.environ["SPOTIFY_OAUTH_CLIENT_SECRET"] = credentials.SPOTIPY_CLIENT_SECRET
    os.environ["SPOTIFY_OAUTH_REDIRECT_URI"] = credentials.SPOTIPY_REDIRECT_URI


register_environment_variables()


class Config:
    """Flask configuration settings."""

    # Flask
    SECRET_KEY = os.environ.get("APP_SECRET_KEY") or "you-will-never-guess"

    # Spotify
    # SPOTIPY_SCOPES = ["playlist-modify-private", "playlist-modify-public", "user-top-read"]
    SPOTIFY_OAUTH_CLIENT_ID = os.environ.get("SPOTIFY_OAUTH_CLIENT_ID")
    SPOTIFY_OAUTH_CLIENT_SECRET = os.environ.get("SPOTIFY_OAUTH_CLIENT_SECRET")
    SPOTIFY_OAUTH_REDIRECT_URI = os.environ.get("SPOTIFY_OAUTH_REDIRECT_URI")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


## App setup

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "spotify.login"


## OAuth


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


spotify_blueprint = make_spotify_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

@oauth_authorized.connect_via(spotify_blueprint)
def spotify_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = blueprint.session.get("/v1/me")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    info = resp.json()
    user_id = info["id"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.")

    else:
        # Create a new local user account for this user
        user = User(
            spotify_id=info["id"],
            username=info["display_name"],
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(spotify_blueprint)
def spotify_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")

app.register_blueprint(spotify_blueprint, url_prefix="/spotify_login")

## Routes

# @app.route("/")
# def index():
#     return "<h1>Index</h1>"


@app.route("/login")
def spotify_login():
    if not spotify.authorized:
        return redirect(url_for("spotify.login"))

    account_info = spotify.get("/v1/me")

    if account_info.ok:
        account_info_json = account_info.json()
        return f"</h1>You are logged in, {account_info_json['display_name']}."

    return "<h1>Request failed!</h1>"


@app.route("/discover-weekly-enhanced")
@login_required
def discover_weekly_enhanced():
    return (
        f"<h1>Here is where the main functionality will exist, {current_user.username}"
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


## Run

if __name__ == "__main__":
    register_environment_variables()

    app.run(debug=True)
