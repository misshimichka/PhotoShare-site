from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Don't forget me")
    submit = SubmitField('Log In')