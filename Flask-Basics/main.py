from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "any secret key"

class NameForm(FlaskForm):
    name = StringField("what is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
        name = form.name.data
        form.name.data = ''
    return render_template("name.html", name = name, form = form )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)