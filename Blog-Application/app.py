from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone, date
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = "any secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'hafsaamanan@gmail.com'
app.config['MAIL_PASSWORD'] = 'ybynjtaixkmdbmci'
app.config['MAIL_DEFAULT_SENDER'] = 'hafsaamanan@gmail.com'
mail = Mail(app)

db = SQLAlchemy(app)
migrate =  Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Submit")

class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    fav_color = StringField("Favourite Color")
    password_hash = PasswordField("Password", validators=[DataRequired(),EqualTo('password_hash2',message = 'Password does not match')])
    password_hash2 = PasswordField("Confirm Password", validators = [DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

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
    #author = db.Column(db.String(255))
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
    
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'

@app.route('/name', methods = ['GET','POST'])
def name():
    name = None 
    form = NameForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data)
            user = Users(username = form.username.data, name=form.name.data, email=form.email.data, fav_color = form.fav_color.data, password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.fav_color.data = ''
        form.password_hash.data = ''
        flash("Form submitted successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("name.html", name = name, form = form, our_users = our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = NameForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.username = request.form['username']
		name_to_update.email = request.form['email']
		name_to_update.fav_color = request.form['fav_color']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update, id= id)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update)
	else:
		return render_template("update.html", 
				form=form,
				name_to_update = name_to_update)
    
@app.route('/delete/<int:id>')
def delete(id):
    name  = None
    form = NameForm()
    user_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted successfully!!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("name.html", name = name, form = form, our_users = our_users)
    
    except:
        flash("Oops there was a problem deleting!!")
        return render_template("name.html", name = name, form = form, our_users = our_users)

@app.route('/add-post', methods = ['GET','POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please Login in order to comment")
            return redirect(url_for('login'))
        poster = current_user.id
        post = Posts(title=form.title.data, poster_id = poster, content = form.content.data, slug = form.slug.data)
        form.title.data = ''
        #form.author.data = ''
        form.content.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Blog submitted successfully")

    return render_template('add_post.html', form = form)

@app.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)  # Get the page number from the URL query parameter, default to 1
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=3)  # Paginate the query
    # page = request.args.get('page', 1, type=int)
    # posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    # posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html',posts=posts)

@app.route('/post/<int:id>',methods = ['GET','POST'])
def post(id):
    post = Posts.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please Login in order to comment")
            return redirect(url_for('login'))
        #poster = current_user.id
        email = post.poster.email
        body = form.content.data
        comment = Comments(content=form.content.data, commentor_id = current_user.id, post_id = id)
        form.content.data = ''
        db.session.add(comment)
        db.session.commit()
        msg = Message('New Comment', recipients = [email],body = body)
        mail.send(msg)
        flash("Comment added successfully")
        return redirect(url_for('post', id=id))
    comments = Comments.query.filter_by(post_id=id).order_by(Comments.date_posted.desc()).all() 
    return render_template('post.html', post=post, form=form,comments = comments)

@app.route('/posts/edit/<int:id>', methods = ['GET','POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        #post.author = form.author.data
        post.content = form.content.data
        post.slug = form.slug.data
        db.session.add(post)
        db.session.commit()
        flash("Post Has been updated ")
        return redirect(url_for('post',id = post.id))
    if current_user.id == post.poster_id:
        form.title.data = post.title
        #form.author.data = post.author
        form.content.data = post.content
        form.slug.data = post.slug
        return render_template('edit_post.html', form = form)
    else:
        flash("You arent authorized to edit this post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('edit_post.html', form=form)

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id: 
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted successfully")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html',posts=posts)

        except:
            flash("There was a problem deleting")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html',posts=posts)
    else:
        flash("You arent authorized to delete that post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NameForm()
    id = current_user.id
    name_to_update =  Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.fav_color = request.form['fav_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update)
    else:
        return render_template("dashboard.html",form=form,name_to_update = name_to_update)
    
    #return render_template('dashboard.html')

@app.route('/user-login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Oops!! Wrong Password")
        else:
            flash("This user does not exist")
    return render_template('user_login.html', form = form)

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('login'))

@app.route('/search', methods = ["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Posts.content.like('%'+ post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html", form=form, searched = post.searched, posts = posts)

    
@app.context_processor
def base():
    form = SearchForm()
    return dict(form = form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)