import os

import credentials

def register_environment_variables() -> None:
    """Register environment variables for Spotipy and Flask."""
    
    # Spotipy
    os.environ["SPOTIPY_CLIENT_ID"] = credentials.SPOTIPY_CLIENT_ID
    os.environ["SPOTIPY_CLIENT_SECRET"] = credentials.SPOTIPY_CLIENT_SECRET
    os.environ["SPOTIPY_REDIRECT_URI"] = credentials.SPOTIPY_REDIRECT_URI
    
    # Flask
    os.environ["APP_SECRET_KEY"] = credentials.APP_SECRET_KEY
