# pylint: disable = missing-function-docstring
# pylint: disable = invalid-name

import time
from typing import Any

from flask import Flask, request, session, redirect
from flask.sessions import SessionMixin

import spotipy

SCOPES = ["playlist-modify-private", "playlist-modify-public", "user-top-read"]

app = Flask(__name__)

app.secret_key = "SessionSecretKey"


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/callback")
def callback():

    # will enable once callback does things.
    # sp_oauth = spotipy.oauth2.SpotifyOAuth(scope=SCOPES)
    session.clear()
    code = request.args.get("code")
    # token_info = sp_oauth.get_access_token(code)
    session["token_info"] = {"code": code} # change for `token_info`

    title = "<h1>You successfully logged in to Spotify!</h1>"
    msg = "<p>You can go back to the application.</p>"
    code_print = f"<p>Code:</p><p>{code}</p>"
    
    return title + msg + code_print

# @app.route("/go", methods=["POST"])
# def go():
#     session['token_info'], authorized = get_token(session)
#     session.modified = True
#     if not authorized:
#         return redirect("/")
#     data = request.form
#     return redirect("/")
    
    
# # Checks to see if token is valid and gets a new token if not
# def get_token(session: SessionMixin) -> tuple[dict[str, Any], bool]:
#     token_valid = False
#     token_info = session.get("token_info", {})

#     # Checking if the session already has a token stored
#     if not session.get('token_info', False):
#         token_valid = False
#         return token_info, token_valid

#     # Checking if token has expired
#     now = int(time.time())
#     is_token_expired = session.get('token_info').get('expires_at') - now < 60

#     # Refreshing token if it has expired
#     if is_token_expired:
#         # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
#         sp_oauth = spotipy.oauth2.SpotifyOAuth(scope = SCOPES)
#         token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

#     token_valid = True
#     return token_info, token_valid


if __name__ == "__main__":
    app.run(debug=True)
