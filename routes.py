from flask import render_template, url_for

from data_test import send_post, create_user
from main import app
from post import Post


@app.route('/')
def start():
    send_post('Kris', 'atata')
    return render_template('common/news_line.html')


@app.route('/create_account')
def create_account():
    return render_template('common/create_account.html')


@app.route('/news_line')
def news_line():
    return render_template('common/news_line.html')


@app.route('/post')
def post():
    return render_template('common/post.html')


@app.route('/user_posts')
def user_posts():
    posts = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g')
    return render_template('user/user_posts.html', posts=posts)


@app.route('/profile')
def profile():
    posts = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g')
    return render_template('user/profile.html', posts=posts)
