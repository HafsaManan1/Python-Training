from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

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

# class PasswordForm(FlaskForm):
#     email = StringField("Email", validators=[DataRequired()])
#     password_hash = PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Submit")