# FTA Unofficial API
Python3 script that fetches FTA server for student schedules, parses data into a dict/json format. 

#### Python library dependancies
+ requests
+ bs4
+ flask

#### How to use?
Send a HTTP GET request with the student alias appended at the end of URL to the server where it is hosted. Currently, the server is hosted at:
<a target="_blank" href="http://ftaapi-fta-pi.1d35.starter-us-east-1.openshiftapps.com/">OpenShift</a>.

##### Example
To get Bob's upcomming flights, you will need to send the following HTTP request:
http://ftaapi-fta-pi.1d35.starter-us-east-1.openshiftapps.com/<BOB's Alias>

Thus:

http://ftaapi-fta-pi.1d35.starter-us-east-1.openshiftapps.com/bob123

#### The Get response
The server responds in the form of Json. It contains a top level key "Return" and the value contains one dictionary for each flights.An example response would be:

{"Return":[{"AIRCRAFT":"YTQ","CAPITAN":"Mike","CREW":"Charles","DATE":"10/10/2010T07:20","DESCRIPTION":"Circuits","EXCERCISE":"07","FLY_TYPE":"Dual","MODULE":"1"}]}

The server may respond with errors:

For example, when length of alias is < 4 the response would be:
{"ERROR": "Invalid Alias: length < 4"}

##### List of things to do
+ Return errors from FTA server, eg. user credential errors and etc. 


##### Things to keep in mind:
+ Order of flights: The Json data does not have flights in order of time and date.
+ Date and Time: It is formated %day%/%month%/%year%T%Hour%:%Minute%


#### Server restrictions
The server is hosted on a free account, as result of this it is limitted by:
+ 1 cpu and 1GB of memory
+ Resource Hibernation: Per Openshift Starter Plan description, "Your project resources sleep after 30 minutes of inactivity, and must sleep 18 hours in a 72 hour period".





