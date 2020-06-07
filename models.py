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

    posts = db.relationship('Post', backref='users')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<User: {self.get_full_name()}>'


class Post(db.Model):
    """ Post model """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(30), nullable=False)

    content = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    
    # tags = db.relationship('Tag', secondary='post_tag', backref=db.backref('post_tag', lazy='dynamic'))
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')


    def __repr__(self):
        return f'<Post: {self.title} by {self.users.get_full_name()}>'



class Tag(db.Model):
    """ Tag model """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return f'<Tag: {self.name}>'



class PostTag(db.Model): 
    __tablename__ = 'post_tag'
    
    # __table_args__ = (
    #     db.PrimaryKeyConstraint("post_id", "tag_id"),
    # )
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'), primary_key=True)
    
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='cascade'), primary_key=True)
