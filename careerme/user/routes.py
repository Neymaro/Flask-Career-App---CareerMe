from flask import Blueprint,render_template,redirect
from careerme.user.forms import (RegisterCompany,RegisterUser)

user = Blueprint('user',__name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    userform = RegisterUser()
    companyform = RegisterCompany()

    return render_template('register.html',title='Register',userform=userform,companyform=companyform)


@user.route("/login")
def login():
    return render_template('login.html',title="Login")