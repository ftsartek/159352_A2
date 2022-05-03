from app import app
from flask_wtf import FlaskForm, csrf
from wtforms import TextAreaField, SelectField, BooleanField, DateField, StringField, PasswordField, IntegerField, validators

csrf = csrf.CSRFProtect(app)


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=4, max=30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=25)])


class RegistrationForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=4, max=30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=25)])
    confirm = PasswordField('Confirm Password', [validators.DataRequired(), validators.Length(min=8, max=25)])
