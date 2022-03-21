import time
from typing import Union, Any

import spotipy as sp

from flask.sessions import SessionMixin

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
