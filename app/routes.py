# pylint: disable = missing-function-docstring
# pylint: disable = invalid-name

import json

from flask import request, session, redirect, render_template, flash

from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user

import spotipy as sp

from app.models import Playlist
from app.views import render_playlist, seconds_to_mm_ss

from app.oauth.scripts import get_token
from app.oauth.forms import get_login_form
from app.oauth.models import OAuth

from app import app, db, spotify_bp, spotify

## DEV

with open("samples/playlist.json", encoding="utf-8") as f:
    test_playlist_response = json.load(f)
    
authorized = False


spotify_bp.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user)



@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def home():
    # if not spotify.authorized:
    #     flash("You are not authorized.")
    nav_form = get_login_form(authorized)
    return render_template("home.html", nav_form=nav_form)


@app.route("/about", methods=["GET", "POST"])
def about():
    nav_form = get_login_form(authorized)
    return render_template("about.html", nav_form=nav_form)


@app.route("/discover_enhanced", methods=["GET", "POST"])
def discover_enhanced():
    nav_form = get_login_form(authorized)

    playlist = Playlist.from_response(test_playlist_response)

    total_duration = int(sum(playlist.track_duration))

    cover = playlist.get_cover_url(300)

    return render_template(
        "discover_enhanced.html",
        table=render_playlist(playlist.summary()),
        cover=cover,
        total_duration=seconds_to_mm_ss(total_duration),
        nav_form=nav_form,
    )


@app.route("/callback")
def callback():
    nav_form = get_login_form(authorized)

    # will enable once callback does things.
    # sp_oauth = sp.oauth2.SpotifyOAuth(scope=SCOPES)
    session.clear()
    code = request.args.get("code")
    # token_info = sp_oauth.get_access_token(code)
    session["token_info"] = {"code": code}  # change for `token_info`

    return render_template("callback.html", code=code, nav_form=nav_form)


# # authorization-code-flow Step 1. Have your application request authorization;
# # the user logs in and authorizes access
# @app.route("/")
# def verify():
#     # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
#     sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = CLI_ID, client_secret = CLI_SEC, redirect_uri = REDIRECT_URI, scope = SCOPE)
#     auth_url = sp_oauth.get_authorize_url()
#     print(auth_url)
#     return redirect(auth_url)

# @app.route("/index")
# def index():
#     return render_template("index.html")

# # authorization-code-flow Step 2.
# # Have your application request refresh and access tokens;
# # Spotify returns access and refresh tokens
# @app.route("/api_callback")
# def api_callback():
#     # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
#     sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = CLI_ID, client_secret = CLI_SEC, redirect_uri = REDIRECT_URI, scope = SCOPE)
#     session.clear()
#     code = request.args.get('code')
#     token_info = sp_oauth.get_access_token(code)

#     # Saving the access token along with all other token related info
#     session["token_info"] = token_info


#     return redirect("index")


# # authorization-code-flow Step 3.
# # Use the access token to access the Spotify Web API;
# # Spotify returns requested data
# @app.route("/go", methods=['POST'])
# def go():
#     session['token_info'], authorized = get_token(session)
#     session.modified = True
#     if not authorized:
#         return redirect('/')
#     data = request.form
#     sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
#     response = sp.current_user_top_tracks(limit=data['num_tracks'], time_range=data['time_range'])

#     # print(json.dumps(response))

#     return render_template("results.html", data=data)


# # Checks to see if token is valid and gets a new token if not
# def get_token(session_: SessionMixin) -> tuple[dict[str, Any], bool]:
#     token_valid = False
#     token_info = session_.get("token_info", {})

#     # Checking if the session already has a token stored
#     if not session_.get("token_info", False):
#         token_valid = False
#         return token_info, token_valid

#     # Checking if token has expired
#     now = int(time.time())
#     is_token_expired = session_.get("token_info").get("expires_at") - now < 60

#     # Refreshing token if it has expired
#     if is_token_expired:
#         # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
#         sp_oauth = sp.oauth2.SpotifyOAuth(scope=SCOPES)
#         token_info = sp_oauth.refresh_access_token(
#             session_.get("token_info").get("refresh_token")
#         )

#     token_valid = True
#     return token_info, token_valid


if __name__ == "__main__":
    app.run(debug=True)
