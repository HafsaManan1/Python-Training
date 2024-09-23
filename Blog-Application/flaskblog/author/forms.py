from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError

# Custom validator to check if password is alphanumeric
def is_alphanumeric(form, field):
    if not field.data.isalnum():
        raise ValidationError('Password must contain only alphanumeric characters.')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5), is_alphanumeric])
    submit = SubmitField("Login")

class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=100)])
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    bio = TextAreaField("Bio", validators=[Length(max=500)])
    profile_pic = FileField("Profile Pic")
    password_hash = PasswordField("Password", validators=[
        DataRequired(), 
        Length(min=6), 
        is_alphanumeric, 
        EqualTo('password_hash2', message="Passwords must match.")
    ])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RestRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=100)])
    submit = SubmitField("Reset Password")

class RestPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6),
        is_alphanumeric
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')
    ])
    submit = SubmitField('Reset Password')
