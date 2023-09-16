import json
import random

from flask import render_template

import main
from database import User, db


def show_my_profile(login):
    user = User.query.filter_by(username=login).first()
    main.current_user = user
    user_links = prepare_user_links(user)
    return render_template('user/my_profile.html', user=user, user_links=user_links,
                           profile_holder=main.current_user)


def create_user(login, password):
    user = User(username=login, password=password, user_photo='simple_server/users_photos/default_photo.jpg',
                followers='', subscriptions='')
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        print('Saving data error')


def load_image():
    """
    image loading imitation, return path - link imitation
    """
    num = random.randint(1, 41)
    return f'simple_server/img/{num}.jpg'


def get_new_user_photo():
    """
    new user photo loading imitation, return path - link imitation
    """
    num = random.randint(1, 10)
    return f'simple_server/users_photos/default_photo_{num}.jpg'


def get_all_posts():
    users = User.query.all()
    posts = []
    for user in users:
        user_posts = user.posts
        if user_posts is not None:
            user_posts = json.loads(user_posts)
            user_posts = user_posts.values()
            number = 1
            for user_post in user_posts:
                user_post['username'] = user.username
                user_post['user_photo'] = user.user_photo
                user_post['number'] = number
                number += 1
                posts.append(user_post)
    return posts


def prepare_user_links(user):
    if user.posts is None:
        posts_amount = 0
    else:
        posts = json.loads(user.posts)
        posts_amount = len(posts.keys())
        user.posts = posts.values()
        number = 1
        for user_post in user.posts:
            user_post['number'] = str(number)
            number += 1
    if user.followers == '':
        followers_amount = 0
    else:
        followers_amount = len(user.followers.split('&')) - 1
    if user.subscriptions == '':
        subs_amount = 0
    else:
        subs_amount = len(user.subscriptions.split('&')) - 1
    return {'posts_amount': posts_amount, 'followers_amount': followers_amount, 'subscriptions_amount': subs_amount}


# new_post = Post(load_image(), 'new photo', 'new post and photo')
# send_post('Alina', new_post)

# user = User.query.filter_by(username='Stefan').first()
# user.posts = None
# db.session.commit()
