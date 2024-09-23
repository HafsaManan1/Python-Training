from flaskblog import db
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False,unique = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False,unique = True)
    fav_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Posts', backref = 'poster')
    comments = db.relationship('Comments', backref = 'commenter')

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
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comments', backref='post')

class Comments(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    content = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    commentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))