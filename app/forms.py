from app import app
from flask_wtf import FlaskForm, csrf
from wtforms import TextAreaField, SelectField, BooleanField, DateField, StringField, PasswordField, IntegerField, \
    validators, HiddenField, BooleanField, SubmitField

csrf = csrf.CSRFProtect(app)


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=25)])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(), validators.equal_to('confirm', message="Password & Confirm field inputs did not match."), validators.Length(min=6, max=25)])
    confirm = PasswordField('Confirm Password', [validators.InputRequired()])
    first_name = StringField('First Name', [validators.DataRequired()])
    surname = StringField('Surname', [validators.DataRequired()])
    submit = SubmitField("Register")


class AircraftEditForm(FlaskForm):
    id = HiddenField('Aircraft ID')
    model = HiddenField('Aircraft Model')
    registration = StringField('Aircraft Registration', [validators.DataRequired(), validators.Length(min=4, max=10)])
    capacity = IntegerField('Aircraft Capacity', [validators.DataRequired(), validators.NumberRange(1, 1000)])
    retired = BooleanField('Retired')
    maint_schedule = DateField('Maintenance Due', [validators.DataRequired()])
    submit = SubmitField("Save Changes")


class ValidationCheckForm(FlaskForm):
    validation_code = StringField('Validation Code', [validators.DataRequired()])
    submit = SubmitField("Validate Account")
