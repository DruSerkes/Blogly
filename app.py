"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag
from helpers import tag_post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ajgiojagoiajgoia'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    posts = Post.query.all()
    posts = posts[-5:]

    users = User.query.all()
    return render_template('/home.html', posts=posts, users=users)

# USER ROUTES 
@app.route('/users')
def list_users():
    """ Show list of users """
    users = User.query.order_by(User.last_name).all()
    return render_template('base.html', users=users)


@app.route('/users/new')
def show_add_user_form():
    """ Display form to add a user """
    return render_template('add_user.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    """ Add a user """
    first = request.form['first-name']
    last = request.form['last-name']
    url = request.form.get('url', None)

    user = User(first_name=first, last_name=last, image_url=url)
    db.session.add(user)
    db.session.commit()

    return redirect('/')


@app.route('/users/<int:user_id>')
def display_user(user_id):
    """ Display a user """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('/user.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """ Display form to edit a user """
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """ Edit a user """
    first = request.form['first-name']
    last = request.form['last-name']
    url = request.form.get('url', None)

    user = User.query.get_or_404(user_id)
    user.first_name = first
    user.last_name = last
    user.image_url = url

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ Delete a user """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')


# BLOG POST ROUTES 
@app.route('/users/<int:user_id>/posts/new')
def create_post_form(user_id):
    """ Display form to create a post """ 
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """ Create a post and redirect to user page """
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    tag_post(tags, post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def display_post(post_id):
    """ Display a post """
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)
    return render_template('post.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """ Display form to edit a post """
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ Edit a post """
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    tag_post(tags, post)


    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ Delete a post """
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/users')


# TAG ROUTES

@app.route('/tags')
def display_all_tags():
    """ Display page with list of tags """ 
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('/tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def display_tag(tag_id):
    """ Display details about a tag (lists all posts with tag) """
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.post_tag
    return render_template('/show_tag.html', posts=posts, tag=tag)

@app.route('/tags/new')
def create_tag_form():
    """ Display form to create new tag """
    return render_template('/add_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """ Creates new tag and redirects to tag list """
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """ Display form to edit tag """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """ Edits a tag """
    name = request.form['name']

    tag = Tag.query.get_or_404(tag_id)
    tag.name = name

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """ Deletes a tag and redirects to tag list """
    Tag.query.filter(Tag.id == tag_id).delete()
    return redirect('/tags')
