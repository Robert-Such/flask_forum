from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_created}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), default='None')
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    view_count = db.Column(db.Integer, unique=False, nullable=False, default=0)
    upvote_count = db.Column(db.Integer, unique=False, nullable=False, default=0)
    downvote_count = db.Column(db.Integer, unique=False, nullable=False, default=0)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    upvotes = db.relationship('Upvote', backref='post', lazy=True)
    downvotes = db.relationship('Downvote', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    upvote_count = db.Column(db.Integer, unique=False, nullable=False, default=0)
    downvote_count = db.Column(db.Integer, unique=False, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    upvotes = db.relationship('Upvote', backref='comment', lazy=True)
    downvotes = db.relationship('Downvote', backref='comment', lazy=True)

    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"


class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def __repr__(self):
        return f"Post('{self.id}', '{self.date_posted}')"

class Downvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def __repr__(self):
        return f"Post('{self.id}', '{self.date_posted}')"
