Firstly execute the script db_intialise.py. This file creates the necessary tables. The schema of the above database is listed in schemas.sql. 

Execution with uwsgi only: 

To exceute via wsgi without nginx, add the following commands  to the wsgi.ini file. 
			socket 127.0.0.1:5001
			protocol http

The type the following command in the  terminal
	uwsgi --ini wsgi.ini


Exectuion with nginx and wsgi:

	1 execute uwsgi using  the ini file as stated above
	2 Run nginx
	3 visit 127.0.0.1 to access the website

Error Not resolved: I still did not succeed in integrating uwsgi and nginx, though both of them run independently. Take a look at the nginx log files. 



