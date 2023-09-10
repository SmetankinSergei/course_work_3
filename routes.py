import json

from flask import render_template, request

import main
from utils import *

from checks import check_auth_data, check_reg_data
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
                user_links = prepare_user_posts(user)
                return render_template('user/my_profile.html', user=user, user_links=user_links,
                                       profile_holder=main.current_user)
            else:
                return render_template('common/fail_authorization.html')
        elif request.form.get('registration') == 'registration':
            if check_reg_data(login, password):
                create_user(login, password)
                user = User.query.filter_by(username=login).first()
                main.current_user = user
                user_links = prepare_user_posts(user)
                return render_template('user/my_profile.html', user=user, user_links=user_links,
                                       profile_holder=main.current_user)
            else:
                return render_template('common/fail_authorization.html')
    else:
        return render_template('common/authorization.html')


@app.route('/my_profile')
def my_profile():
    user_links = prepare_user_posts(User.query.filter_by(username=main.current_user.username).first())
    return render_template('user/my_profile.html', user=main.current_user, user_links=user_links,
                           profile_holder=main.current_user)


@app.route('/users_list/<string:list_name>/<string:username>')
def users_list(list_name, username):
    user = User.query.filter_by(username=username).first()
    users = []
    if list_name == 'Followers':
        for username in user.followers.split('&')[:-1]:
            users.append(User.query.filter_by(username=username).first())
    elif list_name == 'Subscriptions':
        for username in user.subscriptions.split('&')[:-1]:
            users.append(User.query.filter_by(username=username).first())
    return render_template('user/users_list.html', list_name=list_name, user=main.current_user, profile_holder=user,
                           users=users)


@app.route('/edit_profile')
def edit_profile():
    return render_template('user/edit_profile.html', user=main.current_user)


@app.route('/subscribe/<string:username>', methods=['GET', 'POST'])
def subscribe(username):
    subscribe_on_someone(username, main.current_user.username)
    user = User.query.filter_by(username=username).first()
    user_links = prepare_user_posts(user)
    return render_template('user/profile.html', user=main.current_user, profile_holder=user, user_links=user_links)


@app.route('/news_line')
def news_line():
    return render_template('common/news_line.html', user=main.current_user, posts=get_all_posts())


@app.route('/post/<string:username>/<string:post_number>')
def post(username, post_number):
    user = User.query.filter_by(username=username).first()
    posts = json.loads(user.posts)
    current_post = posts[post_number]
    current_post['views'] = current_post['views'] + 1
    posts[post_number] = current_post
    user.posts = json.dumps(posts)
    db.session.commit()
    print(current_post['views'])
    return render_template('common/post.html', user=main.current_user, profile_holder=user, current_post=current_post,
                           post_number=post_number)


@app.route('/create_post')
def create_post():
    return render_template('user/create_post.html')


@app.route('/user_posts/<string:username>')
def user_posts(username):
    posts = User.query.filter_by(username=username).first().posts
    if posts is not None:
        posts = json.loads(posts).values()
        number = 1
        for one_post in posts:
            one_post['comments_amount'] = len(one_post['comments'])
            one_post['number'] = number
            number += 1
    else:
        posts = 0
    return render_template('user/user_posts.html', user=main.current_user, username=username, posts=posts)


@app.route('/profile/<string:username>')
def profile(username):
    profile_holder = User.query.filter_by(username=username).first()
    user_links = prepare_user_posts(profile_holder)
    prefix = ''
    if username == main.current_user.username:
        prefix = 'my_'
    return render_template(f'user/{prefix}profile.html', user=main.current_user,
                           profile_holder=profile_holder, user_links=user_links)


@app.route('/like/<string:username>/<string:post_number>/<string:current_user_name>')
def like(username, post_number, current_user_name):
    like_action(username, post_number, current_user_name)
    user = User.query.filter_by(username=username).first()
    posts = json.loads(user.posts)
    current_post = posts[post_number]
    return render_template('common/post.html', user=main.current_user, profile_holder=user, current_post=current_post,
                           post_number=post_number)
