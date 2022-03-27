import time
from typing import Union, Any

from flask import flash
from flask.sessions import SessionMixin
from flask_login import login_user
from flask_dance.consumer import oauth_authorized

import spotipy as sp
from sqlalchemy.exc import NoResultFound

from app import db, spotify_bp
from app.oauth.models import User, OAuth

@oauth_authorized.connect_via(spotify_bp)
def spotify_logged_in(blueprint, token:str):
    """Spotify logged in behavior."""
    if not token:
        flash("Failed to log in with Spotify.", category="error")
        return False

    resp = blueprint.session.get("/me")
    if not resp.ok:
        msg = "Failed to fetch user info from Spotify."
        flash(msg, category="error")
        return False

    spotify_info = resp.json()
    spotify_user_id = str(spotify_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=spotify_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=spotify_user_id,
            token=token,
        )

    if oauth.user:
        # If this OAuth token already has an associated local account,
        # log in that local user account.
        # Note that if we just created this OAuth token, then it can't
        # have an associated local account yet.
        login_user(oauth.user)
        flash("Successfully signed in with Spotify.")

    else:
        # If this OAuth token doesn't have an associated local account,
        # create a new local user account for this user. We can log
        # in that account as well, while we're at it.
        user = User(
            # Remember that `email` can be None, if the user declines
            # to publish their email address on Spotify!
            uid=spotify_info["id"],
            name=spotify_info["display_name"],
            email=spotify_info["email"],
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Spotify.")

    # Since we're manually creating the OAuth model in the database,
    # we should return False so that Flask-Dance knows that
    # it doesn't have to do it. If we don't return False, the OAuth token
    # could be saved twice, or Flask-Dance could throw an error when
    # trying to incorrectly save it for us.
    return False

def get_token(session_: SessionMixin, scope:Union[str,list[str]]) -> tuple[dict[str, Any], bool]:
    """Check if token is currently valid and returns new token if there is no token or it is expired."""
    token_valid = False
    token_info = session_.get("token_info", {})

    # Checking if the session already has a token stored
    if not session_.get("token_info", False):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session_.get("token_info").get("expires_at") - now < 60

    # Refreshing token if it has expired
    if is_token_expired:
        # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
        sp_oauth = sp.oauth2.SpotifyOAuth(scope=scope)
        token_info = sp_oauth.refresh_access_token(
            session_.get("token_info").get("refresh_token")
        )

    token_valid = True
    return token_info, token_valid
