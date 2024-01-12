from flask import Blueprint,render_template

main = Blueprint('main',__name__)



@main.route("/")
@main.route("/index")
def home():
    return render_template('index.html')

@main.route("/about")
def about():
    return render_template('about.html',title="About Page")

@main.route("/contact")
def contact():
    return render_template('contact.html',title="Contact Page")