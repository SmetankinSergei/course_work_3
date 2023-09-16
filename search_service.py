import json
from random import choice

import main
from database import User


def get_search_list(search_request, search_mode, amount=10):
    result_list = []
    if search_mode == 'profiles':
        result_list = get_users_by_name(search_request, amount)
    elif search_mode == 'posts':
        result_list = get_posts_by_caption(search_request, amount)
    return result_list


def get_users_by_name(search_request, amount):
    user_id = main.search_session.get_id_for_start()
    last_id = User.query.order_by(User.id.desc()).first().id
    last_valid_id = find_last_valid_id(search_request, last_id, 'profiles')
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


def find_last_valid_id(search_request, last_id, request_type):
    check_id = last_id
    while check_id > 0:
        user = User.query.filter_by(id=check_id).first()
        check_id -= 1
        if user is None:
            continue
        if request_type == 'profiles':
            if search_request in user.username:
                return user.id
        if request_type == 'posts':
            if user.posts is None:
                continue
            user_posts = json.loads(user.posts).values()
            for post in user_posts:
                if search_request in post['caption']:
                    return user.id
    return 0


def get_posts_by_caption(search_request, amount):
    last_id = User.query.order_by(User.id.desc()).first().id
    last_valid_id = find_last_valid_id(search_request, last_id, 'posts')
    result_list = []
    while amount > 0:
        random_id = choice(range(1, last_valid_id))
        user = User.query.filter_by(id=random_id).first()
        user_posts = json.loads(user.posts).values()
        for post in user_posts:
            post['username'] = user.username
            post['user_photo'] = user.user_photo
            result_list.append(post)
            main.search_session.add_item(post)
            amount -= 1
            if amount == 0:
                return main.search_session.get_items_list()
    return main.search_session.get_items_list()
