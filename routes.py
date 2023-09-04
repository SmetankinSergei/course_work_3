import json

from flask import render_template

from data_test import send_post, load_image, get_all_posts, create_user
from database import User
from main import app
from post import Post


@app.route('/')
def start():
    # new_post = Post(load_image(), 'new photo', 'new post and photo')
    # send_post('Alina', new_post)
    return render_template('common/news_line.html')


@app.route('/create_account')
def create_account():
    return render_template('common/create_account.html')


@app.route('/news_line')
def news_line():
    return render_template('common/news_line.html', posts=get_all_posts())


@app.route('/post')
def post():
    return render_template('common/post.html')


@app.route('/create_post')
def create_post():
    return render_template('user/create_post.html')


@app.route('/user_posts/<string:username>')
def user_posts(username):
    print(username)
    posts = User.query.filter_by(username=username).first().posts
    if posts is not None:
        posts = json.loads(posts).values()
    else:
        posts = 0
    print(type(posts))
    return render_template('user/user_posts.html', username=username, posts=posts)


@app.route('/profile/<string:username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user.posts is None:
        posts_amount = 0
    else:
        posts = json.loads(user.posts)
        posts_amount = len(posts.keys())
        user.posts = posts.values()
    return render_template('user/profile.html', user=user, posts_amount=posts_amount)
