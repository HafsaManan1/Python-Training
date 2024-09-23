from flask import render_template, Blueprint
from flaskblog.main.forms import SearchForm

main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home_page():
    form = SearchForm()
    return render_template('main/home.html', form=form)
