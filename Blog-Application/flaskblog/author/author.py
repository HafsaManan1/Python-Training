from flask import Blueprint, render_template, request, flash, redirect, url_for
from flaskblog import db, login_manager
from flaskblog.author.forms import NameForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flaskblog.models import Users, Comments, Posts
from flask_login import login_required, current_user, login_user, logout_user

author = Blueprint("author",__name__)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@author.route('/name', methods = ['GET','POST'])
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

@author.route('/update/<int:id>', methods=['GET', 'POST'])
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
    
@author.route('/delete/<int:id>')
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

@author.route('/dashboard', methods=['GET', 'POST'])
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

@author.route('/user-login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login successful")
                return redirect(url_for('author.dashboard'))
            else:
                flash("Oops!! Wrong Password")
        else:
            flash("This user does not exist")
    return render_template('user_login.html', form = form)

@author.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('author.login'))