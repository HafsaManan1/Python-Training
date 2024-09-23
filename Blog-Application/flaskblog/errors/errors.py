from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

@errors.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@errors.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500