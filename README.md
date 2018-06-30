# BlogPython

This application provides the following functionalities:
 - Register a new user
 - Post a new message with a description and body
 - Like or Unlike a post
 - Edit or delete a posted message(tweet)
 
### Design
 - It is written in python 2.7 using Flask framework
 - Uses Mysqlite as a backend database
 - Uses the Flask "session" object for session management
 - Uses the Flask jinja2 template engine for rendering HTML pages
 
### Installation
 - Install the python libraries mentioned in requirements.txt
 - Execute the script db_intialise.py. This file creates the necessary tables. The schema of the above database is listed in schemas.sql. The name of database file is database.db
 - Pass the port number as an environment variable. The default port is 5001.
 - Execute the script main_application.py
 
