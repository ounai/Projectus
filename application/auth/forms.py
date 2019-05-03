from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min = 3, max = 144)])
    password = PasswordField("Password", [validators.Length(min = 3, max = 144)])

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min = 3, max = 144)])
    password = PasswordField("Password", [validators.Length(min = 3, max = 144)])
    name = StringField("Name", [validators.Length(min = 1, max = 144)])

    class Meta:
        csrf = False

