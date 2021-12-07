To run our project using Visual Studio Code:
 
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