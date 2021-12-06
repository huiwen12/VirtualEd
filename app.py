import os
import time
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request
from flask_mail import Mail, Message
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

#Configure mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "hellovirtualed@gmail.com"
app.config['MAIL_PASSWORD'] = "virtualed"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# flask-mail.Mail(app = None)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

# add db file

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


# List of subjects
subjects = [
    "Arts",
    "Humanities",
    "Language",
    "Life Sciences",
    "Mathematics",
    "Social Sciences"
    "Physica Sciences",
    "Other"  
]
 

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def home():
    """Show home page"""
    if request.method == "POST":
        return redirect("/upload")

    else:
        return render_template("home.html")


# Upload 
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Valid submission
        name = request.form.get("name")
        email = request.form.get("email")
        course_title = request.form.get("course_title")
        subject = request.form.get("subject")
        description = request.form.get("description")
        syllabus = request.form.get("syllabus")


        # Validate name
        if not name:
            return render_template("apology.html", message="Missing name")
        # Validate email
        if not email:
            return render_template("apology.html", message="Missing email")
        if not course_title or not subject or not description or not syllabus:
            return render_template("apology.html", message="Missing required course materials")
    
        # # Add submission to SQL
        #db.execute("INSERT INTO uploads (name, email, course_title, subject, description, syllabus) VALUES (?, ?, ?, ?, ?, ?)", name, email, course_title, subject, description, syllabus)

        # # Send email to the user when upload is successful
        print(email)
        print(type(email))
        message = Message('VirtualEd Upload', sender = 'hellovirtualed@gmail.com', recipients=[email])
        message.body = "Your upload was successful. Thank you for your submission!"
        mail.send(message)

        # # Confirm submission
        return render_template("success.html")

    else:
        return render_template("upload.html", subjects=subjects)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        email_message = request.form.get("email_message")
        if not name or not email or not email_message:
            return render_template("apology.html")
        message = Message('Contact', sender = 'hellovirtualed@gmail.com', recipients=['hchen@college.harvard.edu'])
        message.body = email_message
        mail.send(message)
        return render_template("success.html")
    else:
        return render_template("contact.html")

@app.route("/learn", methods=["POST", "GET"])
def learn():
    if request.method == "POST":
        return render_template("content.html")
    else:
        return render_template("content.html")
# def errorhandler(e):
#     """Handle error"""
#     if not isinstance(e, HTTPException):
#         e = InternalServerError()
#     return apology(e.name, e.code)


# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)

