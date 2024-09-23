from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from wtforms.widgets import TextArea

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")