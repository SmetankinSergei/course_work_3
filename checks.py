import main
from database import User


def check_auth_data(login, password):
    if login == '':
        return False
    users = User.query.all()
    usernames = [user.username for user in users]
    if login in usernames:
        user = User.query.filter_by(username=login).first()
        if password == user.password:
            return True


def check_reg_data(login, password):
    users = User.query.all()
    usernames = [user.username for user in users]
    if login in usernames:
        return False
    else:
        if len(password) < 3:
            return False
    return True
