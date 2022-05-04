from app import app
from flask_wtf import FlaskForm, csrf
from wtforms import TextAreaField, SelectField, BooleanField, DateField, StringField, PasswordField, IntegerField, validators, HiddenField, BooleanField

csrf = csrf.CSRFProtect(app)


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=4, max=30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=25)])


class RegistrationForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=4, max=30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=25)])
    confirm = PasswordField('Confirm Password', [validators.DataRequired(), validators.Length(min=8, max=25)])
    #First name & last name


class AircraftEditForm(FlaskForm):
    id = HiddenField('Aircraft ID')
    model = HiddenField('Aircraft Model')
    registration = StringField('Aircraft Registration', [validators.DataRequired(), validators.Length(min=4, max=10)])
    capacity = IntegerField('Aircraft Capacity', [validators.DataRequired(), validators.NumberRange(1, 1000)])
    retired = BooleanField('Retired')
    maint_schedule = DateField('Maintenance Due', [validators.DataRequired()])
