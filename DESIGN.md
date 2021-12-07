# app.py
We used Flask and Flask-Mail to build our project. Before implementing functions on app.py, we imported libraries that are relevant to our project and configured the mail to send using SSL. We also made a db file called upload.db to store the upload materials.

# HOMEPAGE

For the homepage of our project, we wanted to include a large jumbotron-like banner to capture the attention of the user and garner 
interest regarding VirtualEd and its purpose. To do so, we used the background image bootstrap class, bg-image. We chose “We are 
VirtualEd” as the main text to reflect the foundation of VirtualEd — its community. Users are the main source of content for other 
users, not a third-party authority or distribution service. The phrase “We are VirtualEd” implies that its users are what make up 
the bulk of VirtualEd’s utility. 

Thus, we wanted to make the phrase front and center. Using bootstrap classes and the h1 header tag, we made the phrase large on the jumbotron-like banner.

Next, we wanted the user to be able to learn more about VirtualEd and encourage them to contribute to our repository of course materials. This called for a 2-column format, to split the user’s attention. We used the bootstrap classes “row” and nested div’s of class “col-sm-6” to achieve a 2-column format. In one column, we described our purpose. In the other column, we used an href link to link to the upload page so that users could begin contributing course materials.

# UPLOAD
The upload page is where users can submit new course materials to be displayed on our learn page. We built a form using Flask that allows users to upload their educational content to share with other users on our platform. This form first asks the users for their name and email address, which can be used to contact the user if we have questions about their upload and to send them an email confirmation after their successful submission. For the course content, we display the following input fields on the page: Course Title, Subject, Description, Syllabus, Problem Set, and Other Materials. We require all input fields other than Problem Set and Other Materials because problem sets might not be relevant to humanities courses but are often needed for STEM courses. To easily change the subject options in the event that we want to modify the subject, we decided to create a list of subjects in app.py. Using Jinga on upload.html, we created a for loop that displays each element in the list of subjects as an option on the dropdown menu for the subject. When the user reaches the site through a GET method, the upload page will render with subjects=subjects for the correct options to show up on the dropdown menu. 

When the user clicks the submit button to submit the upload form, that is a POST request to the upload page. On app.py, we store the user input for each input field as a variable. Next, we added logic to validate the user responses to ensure that the 6 required fields are submitted. Pset and other are optional materials on the upload form, so we don’t need to validate those input fields. If the user attempts to submit the upload form without filling out all required fields, the page will return apology.html, which is an error message informing the user that the content has not been submitted. 

Once the validation goes through, we used a SQL query in python to store user input in the table called “uploads.” The variables we created to store each input will be inserted into corresponding columns on the “uploads” table. 

To confirm the submission, we have used Flask-Mail to programmatically send an email to the user if the submission is successful. The email is sent from hellovirtualed@gmail.com to the user’s email, which is the email in the email input field. The email subject is “VirtualEd Upload” and the body message “Your upload was successful. Thank you for your submission!” informs the user that we have received their submission and the uploaded content is also displayed on 

# LEARN
For the learn page, we wanted to let the users search the content by subject. This is to accommodate growth in usage. If we had 
a few courses total, then one would not need to sort by subject; they could view all the courses at once. However, if we end up 
having more courses, then allowing the user to sort by subject makes the page more navigable. We implemented such selection via 
a drop-down menu where users can select a subject. This submits or posts their subject as a value in a form on the learn page. 

This is a POST request to the learn page. On app.py, we used this form input to query all the uploads with the indicated subject. 
These rows are inputted into the subject page. We used jinja to loop through all the courses of a subject and create cards for 
each course. We chose cards to help the courses look approachable, and we implemented the cards via bootstrap documentation. 
Each card has a “learn more” button that inputs the id of the card as a value to the content page.

For clarification: on the backend, we have an SQL table that the upload page populates with the contact information of the 
uploading user and related course information (title, syllabus link, pset link, other, etc.). The learn page searches through 
these same rows. 

The content function takes the id of a course as an input (POSTed from the subject page) and finds the corresponding course 
row in the uploads table. Then, it renders the content template with the course information as an input. Note that, after 
querying, the content variable created is a list of 1 element, and each element is a dictionary with keys that correspond to 
columns of the table. This means that, when inputting the course materials into the content template, one must code 
“content=content[0]” so that the code in the HTML page can successfully index into the course content without indexing into 
the first element of the list every time one wants to display a variable.

All together, the content page displays all the relevant course content, including the course title, description, syllabus 
link, pset link, other materials link, and contact information of the user who uploaded the materials. 

# CONTACT

We would like to provide the user with a way to reach us in case they have any inquiries. The contact page displays a contact form in which the user can submit their name, email, and a message to us. We stored the user input for each field as a variable because we will use the information in app.py. If the user reaches the site via GET request, they will see the contact form. 

When the user submits the contact form, the backend code validates the responses to ensure that all three input fields (name, email, and message) have been filled out. If the responses are valid, we will programmatically send an email from hellovirtualed@gmail.com to our contact email contactvirtualed@gmail.com. The email has a subject titled “VirtualEd Contact From ….” where the name after “From” is the name of the user. The email body includes the email message from the user as well as their email contact information, which allows us to reply to the user through their email address. Lastly, the user will see the success.html page, which confirms that the user has successfully contacted us. 