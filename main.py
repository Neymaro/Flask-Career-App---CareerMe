from flask import Flask , render_template
from careerme.main.routes import main
from careerme.user.routes import user
import os



app = Flask(__name__,template_folder='careerme/templates',static_folder='careerme/static')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.register_blueprint(main,url_prefix="")
app.register_blueprint(user,url_profix="")

@app.route("/")
def home():
    return render_template('index.html')

if __name__ =="__main__":
    app.run(debug=True)