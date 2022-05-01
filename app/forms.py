from wtforms import Form, TextAreaField, SelectField, BooleanField, DateField, StringField, PasswordField, IntegerField, validators


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=4, max=30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=25)])


class RegistrationForm(Form):
    email = StringField('Email', [validators.Length(min=4, max=30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=25)])
    confirm = PasswordField('Confirm Password', [validators.DataRequired(), validators.Length(min=8, max=25)])
