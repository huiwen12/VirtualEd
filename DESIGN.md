# HOMEPAGE

For the homepage of our project, we wanted to include a large jumbotron-like banner to capture the attention of the user and garner 
interest regarding VirtualEd and its purpose. To do so, we used the background image bootstrap class, bg-image. We chose “We are 
VirtualEd” as the main text to reflect the foundation of VirtualEd — its community. Users are the main source of content for other 
users, not a third-party authority or distribution service. The phrase “We are VirtualEd” implies that its users are what make up 
the bulk of VirtualEd’s utility. 

Thus, we wanted to make the phrase front and center. Using bootstrap classes and the h1 header tag, we made the phrase large on the jumbotron-like banner.

Next, we wanted the user to be able to learn more about VirtualEd and encourage them to contribute to our repository of course materials. This called for a 2-column format, to split the user’s attention. We used the bootstrap classes “row” and nested div’s of class “col-sm-6” to achieve a 2-column format. In one column, we described our purpose. In the other column, we used an href link to link to the upload page so that users could begin contributing course materials.

# UPLOAD

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

