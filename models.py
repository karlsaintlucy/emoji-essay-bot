from app import db


class Emoji(db.Model):
    """Model for emojis stored in the database."""

    id = db.Column(db.Integer, primary_key=True)  # pylint:disable=no-member
    emoji = db.Column(db.String(12), unique=True,  # pylint:disable=no-member
                      nullable=False)  # pylint:disable=no-member

    def __repr__(self):
        return '<Emoji %r>' % self.emoji


class FBMessengerMessage(db.Model):
    """Model for message ids from Facebook requests."""

    id = db.Column(db.Integer, primary_key=True)  # pylint:disable=no-member
    message_mid = db.Column(db.String(128), unique=True,  # pylint:disable=no-member
                            nullable=False)

    def __repr__(self):
        return '<FBMessengerMessage %r>' % self.message_mid
