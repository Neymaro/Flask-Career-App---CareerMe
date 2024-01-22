from flask import Blueprint,render_template , request
from careerme.models import JobListing
from careerme import db , app


main = Blueprint('main',__name__)

locations_to_count = ['budapest','madrid','istanbul','copenhagen']

@main.route("/")
@main.route("/index")
def home():
    jobs=JobListing.query.order_by(JobListing.posted_time.desc()).all()
    location_counts = {location: JobListing.query.filter_by(location=location).count() for location in locations_to_count}
    return render_template('index.html',jobs=jobs,location_counts=location_counts)

@main.route("/about")
def about():
    return render_template('about.html',title="About Page")

@main.route("/contact")
def contact():
    return render_template('contact.html',title="Contact Page")


@main.route("/search" , methods=['POST'])
def search():
    search_term=request.form.get('search_term', '').lower()
    results= JobListing.query.filter(db.func.lower(JobListing.title).contains(search_term)).all()
    print(search_term)
    return render_template('search-results.html',results=results, search_term=search_term)