import json
import random

import main
from database import User, db


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


def get_all_posts():
    users = User.query.all()
    posts = []
    for user in users:
        user_posts = user.posts
        if user_posts is not None:
            user_posts = json.loads(user_posts)
            user_posts = user_posts.values()
            for user_post in user_posts:
                user_post['username'] = user.username
                user_post['user_photo'] = user.user_photo
                posts.append(user_post)
    return posts


def prepare_user_posts(user):
    if user.posts is None:
        posts_amount = 0
    else:
        posts = json.loads(user.posts)
        posts_amount = len(posts.keys())
        user.posts = posts.values()
    return posts_amount


def subscribe_on_someone(user_name, follower_name):
    user = User.query.filter_by(username=follower_name).first()
    user.subscriptions += user_name + '&'
    main.current_user.subscriptions = user.subscriptions
    user = User.query.filter_by(username=user_name).first()
    user.followers += follower_name + '&'
    db.session.commit()


# new_post = Post(load_image(), 'new photo', 'new post and photo')
# send_post('Alina', new_post)

# user = User.query.filter_by(username='Stefan').first()
# user.posts = None
# db.session.commit()
