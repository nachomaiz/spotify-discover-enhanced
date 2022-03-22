import os


class Config:
    """Flask configuration settings."""

    SECRET_KEY = os.environ.get("APP_SECRET_KEY") or "you-will-never-guess"
    SPOTIPY_SCOPES = ["playlist-modify-private", "playlist-modify-public", "user-top-read"]