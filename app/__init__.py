from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.spotify import make_spotify_blueprint

from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

spotify_blueprint = make_spotify_blueprint(
    app.config.get("SPOTIPY_CLIENT_ID"),
    app.config.get("SPOTIPY_CLIENT_SECRET"),
    scope=app.config.get("SCOPES"),
    redirect_url=app.config.get("SPOTIPY_REDIRECT_URI"),
)

app.register_blueprint(spotify_blueprint, url_prefix='/login')


# def create_app():
#     """Create a new Flask application."""
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     return app


from app import routes
