import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Flask configuration settings."""
    # Flask
    SECRET_KEY = os.environ.get("APP_SECRET_KEY") or "you-will-never-guess"
    
    # Spotipy
    SPOTIPY_SCOPES = ["playlist-modify-private", "playlist-modify-public", "user-top-read"]
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
