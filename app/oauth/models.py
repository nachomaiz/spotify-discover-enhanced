import sqlalchemy as sql

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    """Load user id."""
    return User.query.get(int(id))

class User(db.Model):
    """User model for database."""
    id: sql.Column = db.Column(db.Integer, primary_key=True)
    uid: sql.Column = db.Column(db.String(255), unique=True)
    name: sql.Column = db.Column(db.String(255))
    email: sql.Column = db.Column(db.String(64), index=True, unique=True, nullable=True)

    def __repr__(self):
        return f"<User {self.uid}>"


class OAuth(OAuthConsumerMixin, db.Model):
    """Oauth consumer database model."""
    user_id: sql.Column = db.Column(db.Integer, db.ForeignKey(User.id))
    provider: sql.Column = db.Column(db.String(64))
    provider_user_id: sql.Column = db.Column(db.String(255))
    token: sql.Column = db.Column(db.String(255))
    user = db.relationship(User)
