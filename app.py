import os
import time
import re

from cs50 import SQL
from flask import Flask, redirect, render_template, request
from flask_mail import Mail, Message
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


#Configure mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "hellovirtualed@gmail.com"
app.config['MAIL_PASSWORD'] = "virtualed"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

# add db file
db = SQL("sqlite:///upload.db")


# List of subjects
subjects = [
    "Arts",
    "Humanities",
    "Language",
    "Life Sciences",
    "Mathematics",
    "Social Sciences",
    "Physical Sciences",
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
        # Variables for submissions
        name = request.form.get("name")
        email = request.form.get("email")
        course_title = request.form.get("course_title")
        subject = request.form.get("subject")
        description = request.form.get("description")
        syllabus = request.form.get("syllabus")
        pset = request.form.get("pset")
        other = request.form.get("other")


        # Validate name
        if not name:
            return render_template("apology.html", message="Missing name")
        # Validate email
        if not email:
            return render_template("apology.html", message="Missing email")
        if not course_title or not subject or not description or not syllabus:
            return render_template("apology.html", message="Missing required course materials")
    
        # # Add submission to SQL
        db.execute("INSERT INTO uploads (name, email, course_title, subject, description, syllabus, pset, other) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            name, email, course_title, subject, description, syllabus, pset, other)

        # # Send email to the user when upload is successful
        message = Message('VirtualEd Upload', sender = 'hellovirtualed@gmail.com', recipients=[email])
        message.body = "Your upload was successful. Thank you for your submission!"
        mail.send(message)

        # # Confirm submission
        return render_template("success.html")

    else:
        return render_template("upload.html", subjects=subjects)

# Allow user to contact us
@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        email_message = request.form.get("email_message")

        # Ensure that the user inputs valid information
        if not name or not email or not email_message:
            return render_template("apology.html")

        # Auto send a contact email through Flask mail
        message = Message('VirtualEd Contact', sender = 'hellovirtualed@gmail.com', recipients=['hchen@college.harvard.edu'])
        message.body = email_message
        mail.send(message)

        # Confirm successful submission
        return render_template("success.html")

    else:
        return render_template("contact.html")

@app.route("/learn", methods=["POST", "GET"])
def learn():
    """Query content by topic."""

    # User reached route via submitting to the /learn page
    if request.method == "POST":

        # If user did not submit a subject for any reason, return an error
        if not request.form.get("subject"):
            return apology("no subject submitted", 400)
        
        # Query courses that are of a certain subject
        uploads = db.execute("SELECT * FROM uploads WHERE subject = ?", request.form.get("subject"))

        # Render subject page to display all courses of a subject
        return render_template("subject.html", uploads=uploads, subject=request.form.get("subject"))

    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("learn.html", subjects=subjects)

@app.route("/content", methods=["POST"])
def content():
    """Get content."""
    
    # User reached route via submitting to the /content page
    if request.method == "POST":

        # If user did not submit a course id for any reason, return an error
        if not request.form.get("id"):
            return apology("no course submitted", 400)

        # Find course by inputted id, return all related information
        content = db.execute("SELECT * FROM uploads WHERE id = ?", request.form.get("id"))

        # Render content page to display all materials of a course
        return render_template("content.html", content=content[0])
