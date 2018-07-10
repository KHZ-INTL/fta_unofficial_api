# FTA Unofficial API
Python3 script that fetches FTA server for student schedules, parses date into a dict/json format. 

#### Python library dependancies
+ requests
+ bs4
+ flask

#### How to use?
Send a HTTP GET request with the student alias appended at the end of URL to the server where it is hosted. Currently, the server is hosted at:
<a target="_blank" href="http://khz13.alwaysdata.net">khz13.alwaysdata.net</a>

##### Example
To get Bob's upcomming flights, you will need to send the following HTTP request:
http://khz13.alwaysdata.net/<BOB's Alias>

Thus:

http://khz13.alwaysdata.net/bob123

#### The Get response
The server responds using Json. It contains a top level key "Return" and the value contains one dictionary for each flights.An example response would be:
{"Return":{"AIRCRAFT":"YTQ","CAPITAN":"Mike","CREW":"Charles","DATE":"10/10/2010T07:20","DESCRIPTION":"Circuits","EXCERCISE":"07","FLY_TYPE":"Dual","MODULE":"1"}}

The server may respond with errors:
For example, when length of alias is < 4 the response would be:
{"ERROR": "Invalid Alias: length < 4"}


##### Things to keep in mind:
+ Order of flights: The Json data does not have flights in order of time and date.
+ Date and Time: It is formated %day/%month/%year %Hour:%Minute


#### Server restrictions
The server is hosted on a free account, as result of this it is limitted by:
+ HTTP response time: the server platform pre-procecess requests using aggressive filters, this may increase the time-to-respond.





