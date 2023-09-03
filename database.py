from flask_sqlalchemy import SQLAlchemy

from main import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    posts = db.Column(db.Text)
    followers = db.Column(db.Text)
    subscriptions = db.Column(db.Text)
