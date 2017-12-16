This is a website hosted at--->>> "http://127.0.0.1:5000/"
running on port 5000

NOTE---> Just run applications.py and go on the url provided above.

NOTE--->  All HTML needs to be in a directory called "Templates"


it has a bunch of functionality->






1. It runs on Flask python framework


2. It uses SQL database to store users and their photos (urls) respectively


3. It queries the databases for form validation, displaying users, removing users, adding photos and removing photos


4. HTML with a touch of JINJA is used at the front end for templating.


5. User can->

	a) Register

	b) Unregister

	c) Add photos

	d) Delete photos

	e) View all the users that have registered (keeping their passwords hidden of course)


6. Name of the database is "gdg.db" which contains 2 tables --->  
"cache" for storing image urls according to registration numbers and "students" to store 
student data like name, registration number and password


7. The templates directory has a bunch of HTML files 