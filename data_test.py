import json
import random

from database import User, db


def create_user():
    user = User(username='Kris', password='123')
    try:
        db.session.add(user)
        db.session.commit()
    except:
        print('Saving data error')


def send_post(username, post):
    # user = User.query.filter_by(username=username).first()
    # user.posts = None
    # db.session.commit()
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


def add_follower(user, follower):
    pass


def add_subscription(user, subscription):
    pass


def load_image():
    """
    image loading imitation, return path - link imitation
    """
    num = random.randint(1, 25)
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
                posts.append(user_post)
    print(posts)
    return posts
