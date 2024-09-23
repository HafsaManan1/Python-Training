from flask import Blueprint, render_template, request, flash, redirect, url_for
from flaskblog import db, login_manager, mail
from flaskblog.author.forms import NameForm, LoginForm, RestRequestForm, RestPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flaskblog.models import Users, PasswordResetToken
from flask_mail import Message
from datetime import datetime, timezone
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
            user = Users(username = form.username.data, name=form.name.data, email=form.email.data, bio = form.bio.data, password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.bio.data = ''
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
		name_to_update.bio = request.form['bio']
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
        name_to_update.bio = request.form['bio']
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

# @author.route('/reset_password', methods = ['GET', 'POST'])
# def reset_request():
#     form = RestRequestForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email = form.email.data).first()
#         if user:
#             flash("Reset request send check your email")
#             return redirect(url_for('author.login'))
         
#     return render_template('reset_request.html', form=form)

@author.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RestRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            token = PasswordResetToken.generate_token(user)
            msg = Message('Password Reset Request',
                          sender='noreply@demo.com',
                          recipients=[user.email])
            msg.body = f'''To reset your password, visit the following link:
            
{url_for('author.reset_password_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.

Regards,
Your Flask App'''
            mail.send(msg)
            flash('An email with instructions to reset your password has been sent.', 'info')
        else:
            flash('No account with that email address exists.', 'warning')
        return redirect(url_for('author.login'))
    return render_template('reset_request.html', form=form)

@author.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    reset_token = PasswordResetToken.query.filter_by(token=token).first_or_404()
    if reset_token.expiration_date.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        flash('The reset token has expired.', 'warning')
        return redirect(url_for('author.reset_request'))

    form = RestPasswordForm()
    if form.validate_on_submit():
        user = reset_token.user
        user.password = form.password.data
        db.session.commit()
        db.session.delete(reset_token)  # Remove the token once used
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('author.login'))
    return render_template('reset_password.html', form=form)