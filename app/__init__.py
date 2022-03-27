from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.spotify import make_spotify_blueprint, spotify

from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

spotify_bp = make_spotify_blueprint(
    app.config.get("SPOTIPY_CLIENT_ID"),
    app.config.get("SPOTIPY_CLIENT_SECRET"),
    scope=app.config.get("SCOPES"),
    redirect_url=app.config.get("SPOTIPY_REDIRECT_URI"),
)

app.register_blueprint(spotify_bp, url_prefix='/login')


# def create_app():
#     """Create a new Flask application."""
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     return app


from app import routes
