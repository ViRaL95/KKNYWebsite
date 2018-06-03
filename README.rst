There are several components to our website. The first are HTML files which provide the structure to our application. CSS allows for styling these HTML Files. Javascript is used to make any requests to the server side code. Javascript is also used to create the affect of animations. 

HTML AND CSS
--------------
templates - A directory for all HTML Files. Several of these HTML files contain portions or segments of HTML code that can be reused. For example notice the navbar.html html file. This file is reused in severalHTML files in order to avoid redundancy.

static - A directory that contains all css, javascript code, images, and documents (KKNY Constitution)
staic/styles - A directory for all your CSS files. There is one main CSS filed named index.css, this css file is used for all HTML files
static/js - A directory for all your Javascript files. 
static/images - A directory for all yimages
static/documents - A directory containing all documents. This can include the KKNY Constitution, flyers etc

EMAIL
-------
A package containing all code that involves sending an email to any KKNY email. For example the python script that sends an email to the KKNY Suggestion Box is here.

DATABASE
--------
A package containing all code that accesses the MongoDB Database. For example when retrieving all committee members the renderMembers module in this package retrieves the members for different committees.

SECRETS
-------
This package contains account information used to retrieve news, the email and password to send an email to the suggestion box. All files in this directory are excluded from the github account using a .gitignore file. This way any secret information does not get out to the public

API
----
This package contains python modules which make requests to any API. For example there is a module in this package which will retrieve all the news for our website. In the future modules that will access paypal or the stubhub api will also be stored here

run.py
-------
This file located in the root directory of the project is used to handle routing in our application. For example when a users goes to the '/members' URI a method renderAllMembers will retrieve all members of different committees in our database. If one would like to add an extra endpoint or URI Please edit this file.

