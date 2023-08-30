from flask import Flask, render_template

app = Flask(__name__)


@app.route('/news_line')
def news_line():
    return render_template('common/news_line.html')


@app.route('/post')
def post():
    return render_template('common/post.html')


@app.route('/user_posts')
def user_posts():
    posts = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g')
    return render_template('user/user_posts.html', posts=posts)


@app.route('/profile')
def profile():
    posts = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c', 'd', 'e', 'f', 'g')
    return render_template('user/profile.html', posts=posts)
