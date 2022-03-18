# pylint: disable = missing-function-docstring
# pylint: disable = invalid-name

import time
from typing import Any
import json

from flask import Flask, request, session, redirect, render_template
from flask.sessions import SessionMixin

import spotipy as sp
import pandas as pd

from scripts.data import Playlist

SCOPES = ["playlist-modify-private", "playlist-modify-public", "user-top-read"]

app = Flask(__name__)

app.secret_key = "SessionSecretKey"

with open("test/samples/playlist.json", encoding="utf-8") as f:
    test_playlist_response = json.load(f)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/discover_enhanced")
def discover_enhanced():
    
    playlist = Playlist.from_response(test_playlist_response).summary()
    playlist["Duration"] = pd.to_datetime(playlist["Duration"], unit='s')
    
    table_render = playlist.style.format({"Duration": lambda s: s.strftime("%M:%S")}).hide_index().to_html(index=False, border=0)
    
    return render_template("discover_enhanced.html", table=table_render)


@app.route("/callback")
def callback():

    # will enable once callback does things.
    # sp_oauth = sp.oauth2.SpotifyOAuth(scope=SCOPES)
    session.clear()
    code = request.args.get("code")
    # token_info = sp_oauth.get_access_token(code)
    session["token_info"] = {"code": code}  # change for `token_info`

    return render_template("callback.html", code=code)


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
#         sp_oauth = sp.oauth2.SpotifyOAuth(scope = SCOPES)
#         token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

#     token_valid = True
#     return token_info, token_valid


if __name__ == "__main__":
    app.run(debug=True)
