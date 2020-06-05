""" Seed file to make sample data for pets db """

from models import User, Post, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If tables aren’t empty, empty them
User.query.delete()
Post.query.delete()
Tag.query.delete()

# Add users
alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Burton')
jane = User(first_name='Jane', last_name='Smith')

# Add new objects to session, so they'll persist
db.session.add(alan)
db.session.add(joel)
db.session.add(jane)


# Commit - otherwise, this never gets saved to db!
db.session.commit()

# Add posts
alan_post = Post(
    title='Birds', content="Birds are pretty and I love them so much", user_id=1)
alan_post2 = Post(
    title='Birds', content="Birds are pretty and I love them so much", user_id=1)
alan_post3 = Post(
    title='Birds', content="Birds are pretty and I love them so much", user_id=1)
joel_post = Post(
    title='Birds', content="Birds are pretty and I love them so much", user_id=2)
jane_post = Post(
    title='Birds', content="Birds are pretty and I love them so much", user_id=3)


# Add to session
db.session.add(alan_post)
db.session.add(alan_post2)
db.session.add(alan_post3)
db.session.add(joel_post)
db.session.add(jane_post)

# Commit
db.session.commit()


# Add Tags 
tag1 = Tag(name='Animals')
tag2 = Tag(name='Bird')
tag3 = Tag(name='West Wing')

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()