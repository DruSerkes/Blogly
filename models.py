"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User model """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    image_url = db.Column(db.String, default=None)

    # posts = db.relationship('Post', cascade='all, delete')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """ Post model """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(30), nullable=False)

    content = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
