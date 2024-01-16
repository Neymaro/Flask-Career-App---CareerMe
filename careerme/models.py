from datetime import datetime
from careerme import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_detail = db.Column(db.Text, nullable=True)
    company_photo = db.Column(db.String(255))  # Assuming you store the path or URL of the photo
    company_email = db.Column(db.String(120), unique=True, nullable=False)
    company_password = db.Column(db.String(60), nullable=False)

    # Establishing a one-to-many relationship with JobListing
    joblistings = db.relationship('JobListing', backref='company', lazy=True)

    def __repr__(self):
        return f"Company('{self.company_name}', '{self.company_email}' , '{self.company_detail}' , '{self.company_password}')"

class JobListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    job_type = db.Column(db.String(50), nullable=True,default="Full Time")
    location = db.Column(db.String(100), nullable=True)
    posted_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Establishing a many-to-one relationship with Company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    def __repr__(self):
        return f"JobListing('{self.title}', '{self.location}', '{self.posted_time}')"
    
class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_fullname=db.Column(db.String(60),nullable=False,default="Anonim")
    worker_email = db.Column(db.String(120), unique=True, nullable=False)
    worker_password = db.Column(db.String(60), nullable=False)
    profile_photo = db.Column(db.String(255))  
    about = db.Column(db.Text)

    def __repr__(self):
        return f"Worker('{self.worker_fullname}','{self.worker_email}' , '{self.worker_password}')"