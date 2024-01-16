from flask import Blueprint,render_template,redirect,flash,url_for
from careerme.forms import (RegisterCompany,RegisterUser)
from careerme.models import Company , Worker
from careerme import bcrypt , db

user = Blueprint('user',__name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    userform = RegisterUser()
    companyform = RegisterCompany()
    if companyform.submitRC.data and companyform.validate():
        if companyform.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(companyform.password.data).decode('utf-8')
            addnewcompany = Company(company_name=companyform.companyname.data,company_email=companyform.email.data,company_password=pw_hash)
            db.session.add(addnewcompany)
            db.session.commit()
            flash(f'Company Name: "{companyform.companyname.data}" Successfully registered!', 'success')
            return redirect(url_for('user.login'))
    if userform.submitRU.data and userform.validate():
        if userform.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(userform.password.data).decode('utf-8')
            addnewworker = Worker(worker_fullname=userform.fullname.data,worker_email=userform.email.data,worker_password=pw_hash)
            db.session.add(addnewworker)
            db.session.commit()
            flash(f'User : {userform.fullname.data} Successfully registered!', 'success')
            return redirect(url_for('user.login'))
    return render_template('register.html',title='Register',userform=userform,companyform=companyform)


@user.route("/login")
def login():
    return render_template('login.html',title="Login")