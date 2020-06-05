"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    return redirect('/users')


@app.route('/users')
def list_users():
    """ Show list of users """
    users = User.query.all()
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
    posts = Post.query.filter(Post.user_id == 1).all()
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


@app.route('/users/<int:user_id>/posts/new')
def create_post_form(user_id):
    user = User.query.get_or_404(id=user_id)
    return render_template('add_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
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
    return render_template('/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ Edit a post """
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ Delete a post """
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/users')
