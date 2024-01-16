from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , EmailField , SubmitField , TextAreaField
from wtforms.validators import InputRequired,Email , EqualTo

class RegisterUser(FlaskForm):
    fullname = StringField('Full Name',[InputRequired("Please enter your name.")])
    email = EmailField('Email',[InputRequired("Please enter your email."),Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    submitRU = SubmitField('Register')


class RegisterCompany(FlaskForm):
    companyname = StringField('Company Name',[InputRequired("Please enter your name.")])
    companyinfo = TextAreaField('About Company')
    email = EmailField('Email',[InputRequired("Please enter your email."),Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    submitRC = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email',[InputRequired("Please enter your email."),Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

