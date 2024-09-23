from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
class SearchForm(FlaskForm):
    searched = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")