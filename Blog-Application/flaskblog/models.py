from flaskblog import db
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False,unique = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False,unique = True)
    bio = db.Column(db.Text(200), nullable = True)
    date_added = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Posts', backref = 'poster', cascade="all, delete-orphan")
    comments = db.relationship('Comments', backref = 'commenter', cascade="all, delete-orphan")
    profile_pic = db.Column(db.String(), nullable = True)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comments', backref='post', cascade="all, delete-orphan")

class Comments(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    content = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    commentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('Users', backref='reset_tokens')

    @staticmethod
    def generate_token(user):
        token = secrets.token_urlsafe()
        expiration_date = datetime.now(timezone.utc) + timedelta(hours=1)
        reset_token = PasswordResetToken(token=token, user=user, expiration_date=expiration_date)
        db.session.add(reset_token)
        db.session.commit()
        return token