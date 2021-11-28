import os
import time
import re

from cs50 import SQL
from app import app 
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

#Configure mail 
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# List of subjects
SUBJECTS = [
    "Arts",
    "Humanities",
    "Language",
    "Life Sciences",
    "Mathematics",
    "Social Sciences"
    "Physica Sciences",
    "Other"  
]
 


@app.route("/")
def home():
    """Show home page"""
    return render_template("index.html")


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
            return render_template("error.html", message="Missing name")
        # Validate email
        if not email:
            return render_template("error.html", message="Missing email")
        if not course_title or not subject or not description or not syllabus:
            return render_template("error.html", message="Missing required course materials")
    
        # Add submission to SQL
        db.execute("INSERT INTO uploads (name, email, course_title, subject, description, syllabus) VALUES (?, ?, ?, ?, ?, ?)", name, email, course_title, subject, description, syllabus)

        # Send email to the user when upload is successful
        message = Message("Your upload was successful. Thank you for your submission!", recipients=[email])
        mail.send(message)

        # Confirm submission
        return render_template("success.html")

    else:
        return redirect("upload.html", subjects=SUBJECTS )
    


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
