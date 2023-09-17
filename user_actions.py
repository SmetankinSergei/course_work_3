import json

from flask import render_template

import main
from database import User, db
from utils import show_my_profile, prepare_user_links


def subscribe_on_someone(user_name, follower_name):
    follower = User.query.filter_by(username=follower_name).first()
    profile_holder = User.query.filter_by(username=user_name).first()
    if user_name not in follower.subscriptions:
        follower.subscriptions += user_name + '&'
        profile_holder.followers += follower_name + '&'
    else:
        follower.subscriptions = follower.subscriptions.replace((user_name + '&'), '')
        profile_holder.followers = profile_holder.followers.replace((follower_name + '&'), '')
    main.current_user.subscriptions = follower.subscriptions
    db.session.commit()


def like_action(username, post_number, current_user_name):
    user = User.query.filter_by(username=username).first()
    posts = json.loads(user.posts)
    if current_user_name in posts[post_number]['likes']:
        posts[post_number]['likes'] = posts[post_number]['likes'].replace(f'{current_user_name}&', '')
    else:
        posts[post_number]['likes'] = posts[post_number]['likes'] + current_user_name + '&'
    user.posts = json.dumps(posts)
    db.session.commit()


def send_post(username, post):
    posts = User.query.filter_by(username=username).first().posts
    user = User.query.filter_by(username=username).first()
    if posts is not None:
        posts = json.loads(posts)
        post_number = max(list(map(lambda key: int(key), posts.keys()))) + 1
    else:
        post_number = 1
        posts = {}
    posts[post_number] = post.get_post_data()
    user.posts = json.dumps(posts)
    db.session.commit()


def change_user_data(new_photo, current_username, new_username):
    user = User.query.filter_by(username=current_username).first()
    user.username = new_username
    user.user_photo = new_photo
    db.session.commit()
    main.current_user = user
