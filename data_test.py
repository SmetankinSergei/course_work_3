import json

from database import User, db
from sqlalchemy import update
from flask_sqlalchemy import SQLAlchemy


def create_user():
    user = User(username='Kris', password='123')
    print(user.username)
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
        post_number = len(posts.keys()) + 1
    else:
        post_number = 1
        posts = {}
    posts[post_number] = post
    posts = json.dumps(posts)
    user.posts = posts
    db.session.commit()


def add_follower(user, follower):
    pass


def add_subscription(user, subscription):
    pass
