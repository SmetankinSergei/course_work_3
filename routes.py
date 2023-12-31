from flask import request

from checks import check_auth_data, check_reg_data
from main import app
from search_service import get_search_list
from user_actions import subscribe_on_someone, like_action, change_user_data
from utils import *
from utils_classes import SearchSession


@app.route('/exit', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def start():
    main.current_user = None
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if request.form.get('authorization') == 'authorization':
            if check_auth_data(login, password):
                return show_my_profile(login)
            else:
                return render_template('common/authorization.html', auth_state='fail')
        elif request.form.get('registration') == 'registration':
            if check_reg_data(login, password):
                create_user(login, password)
                return show_my_profile(login)
            else:
                return render_template('common/authorization.html', auth_state='fail')
    else:
        return render_template('common/authorization.html', auth_state='normal')


@app.route('/my_profile')
def my_profile():
    user_links = prepare_user_links(User.query.filter_by(username=main.current_user.username).first())
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


@app.route('/edit_profile/<string:user_photo>', methods=['GET', 'POST'])
def edit_profile(user_photo):
    if request.method == 'POST':
        if request.form.get('photo') == 'photo':
            user_photo = get_new_user_photo().replace('/', '&&&')
            main.temp_user_photo = user_photo.replace('&&&', '/')
        if request.form.get('edit') == 'edit':
            if main.temp_user_photo is None:
                main.temp_user_photo = user_photo
            new_username = request.form.get('new_username')
            change_user_data(main.temp_user_photo, main.current_user.username, new_username)
            return show_my_profile(new_username)
    return render_template('user/edit_profile.html', user=main.current_user, profile_holder=main.current_user,
                           user_photo=user_photo)


@app.route('/subscribe/<string:username>', methods=['GET', 'POST'])
def subscribe(username):
    subscribe_on_someone(username, main.current_user.username)
    user = User.query.filter_by(username=username).first()
    user_links = prepare_user_links(user)
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
    likes_amount = 0
    if current_post['likes'] != '':
        likes_amount = len(current_post['likes'].split('&')) - 1
    posts[post_number] = current_post
    user.posts = json.dumps(posts)
    db.session.commit()
    return render_template('common/post.html', user=main.current_user, profile_holder=user, current_post=current_post,
                           post_number=post_number, likes_amount=likes_amount)


@app.route('/create_post/<string:photo>')
def create_post(photo):
    return render_template('user/create_post.html', user=main.current_user, photo=photo)


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
    user_links = prepare_user_links(profile_holder)
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
    likes_amount = 0
    if current_post['likes'] != '':
        likes_amount = len(current_post['likes'].split('&')) - 1
    return render_template('common/post.html', user=main.current_user, profile_holder=user, current_post=current_post,
                           post_number=post_number, likes_amount=likes_amount)


@app.route('/search/<string:request_type>', methods=['GET', 'POST'])
def search(request_type):
    if request_type == 'first':
        main.search_session = SearchSession()
    if request.method == 'POST':
        search_request = request.form.get('request')
        search_mode = request.form.get('mode')
        main.search_session.set_request_mode(search_mode)
        main.search_session.set_request(search_request)
        result_list = get_search_list(search_request, search_mode, amount=2)
        return render_template('common/search_result.html', user=main.current_user, profile_holder=main.current_user,
                               search_mode=search_mode, result_list=result_list, search_session=main.search_session)
    return render_template('common/search.html', user=main.current_user, profile_holder=main.current_user)


@app.route('/more_items')
def more_items():
    search_request = main.search_session.get_request()
    search_mode = main.search_session.get_request_mode()
    result_list = get_search_list(search_request, search_mode, amount=2)
    return render_template('common/search_result.html', user=main.current_user, profile_holder=main.current_user,
                           search_mode=search_mode, result_list=result_list, search_session=main.search_session)
