from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , EmailField , SubmitField , TextAreaField , SelectField , IntegerField
from wtforms.validators import InputRequired,Email , EqualTo , ValidationError 
from flask_wtf.file import FileAllowed , FileField
from careerme.models import Worker , Company
from flask import flash

class RegisterUser(FlaskForm):
    fullname = StringField('Full Name',[InputRequired("Please enter your name.")])
    email = EmailField('Email',[InputRequired("Please enter your email."),Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    submitRU = SubmitField('Register')


    def validate_email(self,email):
        company_user = Company.query.filter_by(company_email=email.data).first()
        worker_user = Worker.query.filter_by(worker_email=email.data).first()
        email=company_user or worker_user
        if email:
            raise ValidationError("Someone already registered with this email before.")
    
        

class RegisterCompany(FlaskForm):
    companyname = StringField('Company Name',[InputRequired("Please enter your name.")])
    companyinfo = TextAreaField('About Company')
    email = EmailField('Email',[InputRequired("Please enter your email."),Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    submitRC = SubmitField('Register')

    def validate_email(self,email):
        company_user = Company.query.filter_by(company_email=email.data).first()
        worker_user = Worker.query.filter_by(worker_email=email.data).first()
        email=company_user or worker_user
        if email:
            flash(f'Registration failed!', 'danger')
            raise ValidationError("Someone already registered with this email before.")
            


class LoginForm(FlaskForm):
    email = EmailField('Email',[InputRequired("Please enter your email."),Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class JobAddForm(FlaskForm):
    jobtitle = StringField('Job Title',[InputRequired("Please enter the job title")])
    jobtype = StringField('Job Type')
    jobdescription = TextAreaField('Description')
    joblocation = SelectField('Job Type', choices=[('newyork', 'New York'), ('istanbul', 'Istanbul'), ('budapest', 'Budapest'), ('barcelona', 'Barcelona'), ('madrid', 'Madrid'), ('vienna', 'Vienna'), ('copenhagen', 'Copenhagen'),('other', 'Other')])
    submit = SubmitField('Post Job')


class EditForm(FlaskForm):
    newname = StringField('Profile Name')
    newphoto = FileField('Photo Update',validators=[FileAllowed(['jpg','jpeg','png'])])
    newabout = TextAreaField('About')
    submit = SubmitField('Update')

    def validate_email(self,email):
        company_user = Company.query.filter_by(company_email=email.data).first()
        worker_user = Worker.query.filter_by(worker_email=email.data).first()
        email=company_user or worker_user
        if email:
            raise ValidationError("Someone already registered with this email before.")
        

class CVForm(FlaskForm):
    email = StringField('Email:')
    phone = StringField('Phone Number:')
    location = StringField('Location:')
    degree = StringField('Degree:')
    school = StringField('School:')
    starting_year = IntegerField('Starting Year:')
    graduation_year = IntegerField('Graduation Year (or expected year:)')
    skills = StringField('Skills:')
    submit = SubmitField('Save CV')

