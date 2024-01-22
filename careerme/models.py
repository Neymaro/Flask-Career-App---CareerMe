from datetime import datetime
from careerme import db , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Company.query.get(int(user_id)) or Worker.query.get((int(user_id)))

class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_detail = db.Column(db.Text, nullable=True)
    company_photo = db.Column(db.String(255), default='default.jpg') 
    company_email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    joblistings = db.relationship('JobListing', backref='company', lazy=True)

    def __repr__(self):
        return f"Company('{self.company_name}', '{self.company_email}' , '{self.company_detail}' , '{self.password}')"

class JobListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    job_type = db.Column(db.String(50), nullable=True,default="Full Time")
    location = db.Column(db.String(100), nullable=True)
    posted_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    def __repr__(self):
        return f"JobListing('{self.title}', '{self.location}', '{self.posted_time}')"
    
class Worker(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    worker_fullname=db.Column(db.String(60),nullable=False,default="Anonim")
    worker_email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_photo = db.Column(db.String(255))  
    about = db.Column(db.Text)

    def __repr__(self):
        return f"Worker('{self.worker_fullname}','{self.worker_email}' , '{self.password}')"
    

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(255),default="None")
    school = db.Column(db.String(255),default="None")
    starting_year = db.Column(db.Integer,default="None")
    graduation_year = db.Column(db.Integer,default="None")
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'), nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255),default="None")
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'), nullable=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20),default="None")
    email = db.Column(db.String(255),default="None")
    location = db.Column(db.String(255),default="None")
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'), nullable=False)


class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    educations = db.relationship('Education', backref='cv', lazy=True)
    skills = db.relationship('Skill', backref='cv', lazy=True)
    contact = db.relationship('Contact', backref='cv', uselist=False, lazy=True)

