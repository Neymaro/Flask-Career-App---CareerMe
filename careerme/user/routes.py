import os
import secrets
from PIL import Image
from flask import Blueprint,render_template,redirect,flash,url_for , request , abort
from careerme.forms import (RegisterCompany,RegisterUser,LoginForm , JobAddForm , EditForm , CVForm)
from careerme.models import Company , Worker , JobListing , CV , Education,Skill,Contact
from careerme import bcrypt , db , app, login_manager
from flask_login import login_user , current_user,logout_user,login_required

user = Blueprint('user',__name__)

job_types = {
        'fulltime': 'Full Time',
        'parttime': 'Part Time',
        'Contract': 'Contract' }

@user.route("/register", methods=['GET', 'POST'])
def register():
    userform = RegisterUser()
    companyform = RegisterCompany()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if companyform.submitRC.data and companyform.validate():
        if companyform.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(companyform.password.data).decode('utf-8')
            addnewcompany = Company(company_name=companyform.companyname.data,company_email=companyform.email.data,password=pw_hash,company_detail=companyform.companyinfo.data)
            db.session.add(addnewcompany)
            db.session.commit()
            flash(f'Company Name: "{companyform.companyname.data}" Successfully registered!', 'success')
            return redirect(url_for('user.login'))
    if userform.submitRU.data and userform.validate():
        if userform.validate_on_submit():
            pw_hash = bcrypt.generate_password_hash(userform.password.data).decode('utf-8')
            addnewworker = Worker(worker_fullname=userform.fullname.data,worker_email=userform.email.data,password=pw_hash)
            db.session.add(addnewworker)
            db.session.commit()
            flash(f'User : {userform.fullname.data} Successfully registered!', 'success')
            return redirect(url_for('user.login'))
    return render_template('register.html',title='Register',userform=userform,companyform=companyform)


@user.route("/login" , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        company_user = Company.query.filter_by(company_email=form.email.data).first()
        if company_user is None:
            user = Worker.query.filter_by(worker_email=form.email.data).first()
        else:
            user = company_user

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=form)

@user.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.home'))
    else:
        flash('You have not login yet!!', 'info') 
        return redirect(url_for('user.register'))


@user.route('/account' , methods=['GET', 'POST'])
@login_required
def account():
    company_id_to_query = current_user.id
    job_listings = JobListing.query.order_by(JobListing.posted_time.desc()).filter_by(company_id=company_id_to_query).all()
    show_cv_list = CV.query.filter_by(worker_id=current_user.id).all()   
    if show_cv_list:
        for show_cv in show_cv_list:
            educations = Education.query.filter_by(cv_id=show_cv.id).all()
            skills = Skill.query.filter_by(cv_id=show_cv.id).all()
            contact = Contact.query.filter_by(cv_id=show_cv.id).first()
    else:
        educations = 0
        skills = 0
        contact = 0
    for job_listing in job_listings:
        job_listing.posted_time_str = job_listing.posted_time.strftime('%d/%m/%Y %H:%M')
    form = JobAddForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            jobtype = request.form.get('job_type')
            postnewjob = JobListing(title=form.jobtitle.data,job_type=jobtype
                                    ,content=form.jobdescription.data,
                                    location=form.joblocation.data,company=current_user)
            db.session.add(postnewjob)
            db.session.commit()
            flash(f'You added new job!', 'success')
            return redirect(url_for('main.home'))
    return render_template('account.html', title="My Account" , form=form , 
                           job_types=job_types,job_listings = job_listings , show_cv_list = show_cv_list , educations = educations , skills=skills,contact=contact)


@user.route("/list/<int:list_id>" , methods=['GET', 'POST'])
def post(list_id):
    list = JobListing.query.get_or_404(list_id)
    form = JobAddForm()
    jobtype = request.form.get('job_type')
    if request.method == 'POST':
        if list.company != current_user:
            abort(403)
        if form.validate_on_submit:
            list.title = form.jobtitle.data
            list.content = form.jobdescription.data
            list.location = form.joblocation.data
            db.session.commit()
            flash(f'You updated your listing!', 'success')
            return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.jobtitle.data = list.title
        form.jobdescription.data = list.content
        form.joblocation.data = list.location
    return render_template('list.html', title=list.title, list=list , form=form , job_types=job_types)

@user.route("/list/<int:list_id>/delete" , methods=['GET','POST'])
@login_required
def delete(list_id):
    list = JobListing.query.get_or_404(list_id)
    if list.company != current_user:
         return redirect(url_for('user.login'))
         abort(403)
    db.session.delete(list)
    db.session.commit()
    flash(f'You have succesfully delete your listing!', 'warning')
    return redirect(url_for('user.account'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@user.route("/edit" , methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
            if form.newphoto.data:
                picture_file = save_picture(form.newphoto.data)
                current_user.company_photo = picture_file 
            current_user.company_name = form.newname.data
            current_user.company_detail = form.newabout.data
            db.session.commit()
            flash(f'Successfully Updated!','success')
            return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.newname.data = current_user.company_name
        form.newabout.data = current_user.company_detail
    
    image_file = url_for('static', filename='profile_pics/' + current_user.company_photo)
    return render_template('edit.html',title='Update Profile',form=form,image_file=image_file)



@user.route("/create-cv", methods=['GET','POST'])
@login_required
def createcv():
    form = CVForm()
    if request.method =='POST':
        if form.validate_on_submit:
            create_cv = CV(
                worker_id = current_user.id,
                educations=[Education(degree=form.degree.data,
                                    school=form.school.data,
                                    starting_year=form.starting_year.data,
                                    graduation_year=form.graduation_year.data)],
                skills=[Skill(skill_name=form.skills.data)],
                contact=(Contact(phone=form.phone.data,
                                email=form.email.data,
                                location=form.location.data)))
                
            db.session.add(create_cv)
            db.session.commit()
            flash(f'Successfully Added!','success')
            return redirect(url_for('user.account'))
    return render_template('create-cv.html',title='Cv Create',form=form)



   
