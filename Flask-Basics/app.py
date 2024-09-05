from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = "any secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
migrate =  Migrate(app, db)

class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    fav_color = StringField("Favourite Color")
    submit = SubmitField("Submit")

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False,unique = True)
    fav_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default = datetime.now(timezone.utc))

    def __repr__(self):
        return '<Name %r>' % self.name
    
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'

@app.route('/market')
def market_page():
    items = [
    {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
]
    return render_template('market.html', items=items)

@app.route('/name', methods = ['GET','POST'])
def name():
    name = None 
    form = NameForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, fav_color = form.fav_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.fav_color.data = ''
        flash("Form submitted successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("name.html", name = name, form = form, our_users = our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = NameForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.fav_color = request.form['fav_color']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html", 
				form=form,
				name_to_update = name_to_update)
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
    name = None
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

# @app.route('/name', methods = ['GET','POST'])
# def name():
#     name = None 
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#         flash("Form submitted successfully")
#     return render_template("name.html", name = name, form = form )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)