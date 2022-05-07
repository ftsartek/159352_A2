from app import app, database_helpers
from app.database import Aircraft, Flight, FlightLeg, FlightSchedule
from flask_wtf import FlaskForm, csrf
from wtforms import TextAreaField, SelectField, BooleanField, DateField, StringField, PasswordField, IntegerField, \
    validators, HiddenField, BooleanField, SubmitField

print("Initialising forms")
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


class BookingForm(FlaskForm):
    choice_list = database_helpers.flight_list()
    route_selector = SelectField('Route', [validators.DataRequired()], choices=choice_list)
    date_start_selector = DateField('Between', [validators.DataRequired()])
    date_end_selector = DateField('And', [validators.DataRequired()])
    submit = SubmitField("Search")


class AircraftSelectForm(FlaskForm):
    details = HiddenField('Selection')