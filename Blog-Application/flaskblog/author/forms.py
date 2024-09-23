from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Login")

class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    bio = TextAreaField("Bio")
    password_hash = PasswordField("Password", validators=[DataRequired(),EqualTo('password_hash2',message = 'Password does not match')])
    password_hash2 = PasswordField("Confirm Password", validators = [DataRequired()])
    submit = SubmitField("Submit")

class RestRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Reset Password")

class RestPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
