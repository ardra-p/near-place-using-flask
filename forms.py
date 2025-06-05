from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
print("✔ my_signup_form.py loaded")

class SignupForm(FlaskForm):
    first_name = StringField('First name', validators= [DataRequired("Pleace enter your first name.")])
    last_name = StringField('Last name', validators= [DataRequired("Pleace enter your last name.")])
    email = StringField('Email', validators= [DataRequired("Pleace enter your email."), Email("Pleace enter your valid email")])
    password = PasswordField('Password', validators= [DataRequired("Pleace enter your password."), Length(min=6, message="Password must me 6 characters or more")])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
     email = StringField('Email', validators= [DataRequired("Pleace enter your email."), Email("Pleace enter your valid email")])
     password = PasswordField('Password', validators= [DataRequired("Pleace enter your password."), Length(min=6, message="Password must me 6 characters or more")])
     submit = SubmitField('Sign up')

class AddressForm(FlaskForm):
     address = StringField('Address ', validators=[DataRequired("Please enter your address.")])
     submit = SubmitField("Search")


