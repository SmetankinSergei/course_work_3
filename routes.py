import json

from flask import render_template, request

import main
from checks import check_auth_data, check_reg_data
from data_test import send_post, load_image, get_all_posts, create_user
from database import User
from main import app


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if request.form.get('authorization') == 'authorization':
            if check_auth_data(login, password):
                user = User.query.filter_by(username=login).first()
                main.current_user = user
                # if user.posts is not None:
                #     posts_amount = len(json.loads(user.posts).keys())
                print('auth done!')
                return render_template('user/my_profile.html', user=user)
            else:
                return render_template('common/fail_authorization.html')
        elif request.form.get('registration') == 'registration':
            if check_reg_data(login, password):
                create_user(login, password)
                user = User.query.filter_by(username=login).first()
                main.current_user = user
                return render_template('user/my_profile.html', user=user)
            else:
                return render_template('common/fail_authorization.html')
    else:
        return render_template('common/authorization.html')


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
