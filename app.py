import os.path
from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)
my_users = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_site.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg", "gif"]
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    user_name = db.Column(db.String(20), unique=False, nullable=True)
    password = db.Column(db.String(20), unique=False, nullable=True)
    picture = db.Column(db.String(100), unique=False, nullable=True)
    def __str__(self):
        return f"Name:{self.first_name}, Age:{self.age}"

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        age = request.form.get("age")
        file = request.files.get("filename")
        user_name = request.form.get("username")
        password = request.form.get("password")
        if allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        p = Profile(first_name=first_name, last_name=last_name, age=age, picture=file.filename, user_name=user_name,password=password)
        db.session.add(p)
        db.session.commit()
        my_users.append((first_name, age))
        return redirect("/success")
    return render_template("signup.html")

@app.route("/listUsers")
def listusers():
    users_data = Profile.query.all()
    print("CHECK:",users_data)
    return render_template("listUsers.html", users_data=users_data)

@app.route("/success")
def success():
    return render_template("success.html", my_users=my_users)

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        my_users.append((username))
        user = Profile.query.filter_by(user_name=username, password=password).first()
        if user:
            return redirect("/listUsers")
        else:
            error_message = "Invalid username or password."
            return render_template("login.html", error_message=error_message)
    return render_template("login.html")

@app.route("/homepage")
def hellohome():
    return render_template("homepage.html")

@app.route("/")
def homepage():
    return render_template("homepage.html", my_users=my_users)


if __name__ == "__main__":
    app.run(debug=True)


