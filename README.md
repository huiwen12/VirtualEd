# About
VirtualEd is a Flask app project made by Huiwen Chen and Audrey Chang. This is a Flask web application that aims to increase the accessibility of high-quality education. VirtualEd lets users upload course materials and browse available educational resources; our application also generates emails.
# To run our project using Visual Studio Code:
 
* Download Visual Studio Code and Python3 (or the latest version of Python) on the local computer
* Install the SQLite extension created by alexcvzz and Python extension (if needed) on Visual Studio Code
* Open the project on Visual Studio Code
* Make sure that you have all the requirements listed in Requirements.txt. Follow the following steps if the requirements are not met: 
    * Configure Visual Studio Code to install Flask and activate the virtual environment in the terminal
        $ pip install Flask
        $ . venv/bin/activate
        Refer to the instructions on https://flask.palletsprojects.com/en/2.0.x/installation/ 
* Install cs50 in the terminal
    $ pip install cs50 
* Install Flask-Mail in the terminal 
    $ pip install Flask-Mail 
    Refer to the instructions on https://pythonhosted.org/Flask-Mail/
* If the commands above do not work, try:
    $ pip3 install cs50
    $ python -m pip install --upgrade pip
    $ python -m pip install flask
 
 In your terminal, execute the following commands:
    $ export FLASK_APP=app.py
    $ export FLASK_ENV=development
    $ flask run
    
The website should run on a local host.

# YOUTUBE LINK - website walkthrough
https://youtu.be/sB6NhZ08MvY


To use the web application:
 
* Our Home page displays the purpose of the website and the link to upload course materials to our platform. This page has a description of our prupose to allow users to learn more about the motivation behind our platform.
 
* To navigate the educational resources available on VirtualEd, go to the Learn page and search for educational content by subject. If site users have uploaded course materials for the selected subject, the page will render the content in a card format. Sample course materials have been added to Math, Other, and Social Sciences. Clicking the button on each card will redirect the user to the corresponding course site.
 
* Site users can upload new course materials through the form on the Upload page. The mission of our website is to be an interactive learning platform where users can share their educational resources to make education more accessible, so we appreciate any course uploads from our users, as their contributions can increase the number of educational content on VirtualEd. After submitting the upload form, the user will be redirected to a page that confirms the successful submission and receive an email confirmation from hellovirtualed@gmail.com.
 
* The creators of VirtualEd can be reached by email when site users submit the contact form on our Contact page. The email message and contact information of the user will be sent to contactvirtualed@gmail.com.
