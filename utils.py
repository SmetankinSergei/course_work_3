import json
import random

from flask import render_template

import main
from database import User, db


def get_users_list(search_request, search_mode, amount=10):
    result_list = []
    if search_mode == 'profiles':
        result_list = get_users_by_name(search_request, amount)
    elif search_mode == 'posts':
        result_list = get_posts_by_caption(search_request, amount)
    return result_list


def get_users_by_name(search_request, amount):
    user_id = main.search_session.get_id_for_start()
    last_id = User.query.order_by(User.id.desc()).first().id
    last_valid_id = find_last_valid_id(search_request, last_id)
    users_list = []
    while amount > 0 and last_valid_id >= user_id:
        user = User.query.filter_by(id=user_id).first()
        user_id += 1
        if user is None:
            continue
        elif search_request.lower() in user.username.lower():
            users_list.append(user)
            main.search_session.add_item(user)
            amount -= 1
    if len(users_list) > 0:
        main.search_session.set_id_for_start(users_list[-1].id + 1)
    else:
        main.search_session.set_id_for_start(1)
    if main.search_session.get_id_for_start() <= last_valid_id:
        main.search_session.set_has_more(True)
    else:
        main.search_session.set_has_more(False)
    return main.search_session.get_items_list()


def find_last_valid_id(search_request, last_id):
    check_id = last_id
    while check_id > 0:
        user = User.query.filter_by(id=check_id).first()
        check_id -= 1
        if search_request in user.username:
            return user.id
    return 0


def get_posts_by_caption(search_request, amount):
    return []


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

# new_post = Post(load_image(), 'new photo', 'new post and photo')
# send_post('Alina', new_post)

# user = User.query.filter_by(username='Stefan').first()
# user.posts = None
# db.session.commit()
