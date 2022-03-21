from flask import Flask

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)


# def create_app():
#     """Create a new Flask application."""
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     return app


from app import routes
