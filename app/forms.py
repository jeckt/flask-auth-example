from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=4, max=35)
    ])
    remember_me = BooleanField('remember_me', default=False)

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[
        DataRequired(),
        Length(min=4, max=35)
    ])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=4, max=35),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('repeat')

