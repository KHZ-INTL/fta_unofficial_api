from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import datetime


# Init flask application
app = Flask(__name__)

# Load configs
app.config.from_pyfile('flaskapp.cfg')



class fta():

    def __init__(self, alias):
        self.alias = str(alias)

    def http_get(self):
        """
        HTTP GET page 
        """
        user_id = {'rdUsername': self.alias,
                   'rdFormLogon': 'True',
                   'rdPassword': self.alias,
                   'Submit1': 'Logon'}
        response = requests.post('http://202.158.223.244/OPS_STUDENT_REPORTS/rdPage.aspx', data=user_id)

        if response.status_code != 200:
            return "ERROR: http_get -  {}".format(response.status_code)

        return response.text
    
    def format_date(self, date, method):
        """
        Format date/time to and from iso standard and %d/%m/%YT:%H:%M:%S
        """
        
        if method == "iso":
            date = datetime.datetime.strptime(data, "%d/%m/%y %H:%M").isoformat()
        
        elif method == "display":
            date = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")

        return date 
 


    def parse_html(self, html):
        """
        Parses the table data from html into dictionary
        """
        day = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATUARDAY", "SUNDAY"]
        rem = ["Time", "Captain", "Crew", "Aircraft", "Module", "Exercise", "Description", "Fly Type"]
        schedules_dictionary= {"DATE": "", "CAPITAN": "", "CREW": "", "AIRCRAFT": "", "MODULE": "", "EXCERCISE": "", "DESCRIPTION": "", "FLY_TYPE": ""}

        
        table_data = []
        table_data_without_header = []
        day_index = []
        
        if len(html) == 0:
            return "ERROR: parse_html - len(html) = 0"
        
        soup = BeautifulSoup(html, 'lxml')
        table_rows = soup.find("table").find_all("tr")

        # Extract table data from table 
        for tr in table_rows:
            td = tr.find_all("td")
            for i in td:
                table_data.app(i.text)
        
        # Remove table headers
        for i in table_data:
            if i in rem or i == "":
                continue
            else:
                table_data_without_header.append(i)

        # Extract index of date
        for td in table_data_without_header:
            for d in day:
                if d in str(td):
                    day_index.append((table_data_without_header.index(td)))
       
       # Populate schedules_dictionary The return dictionary
        for a in day_index:
            date_time = table_data_without_header[a].split("-", 2)[1].replace(" ", "")
            date_time = date_time + " " + table_data_without_header[a + 1]
            schedules_dictionary["DATE"] = str(self.format_date(date_time, "iso"))

            if ":" in table_data_without_header[(a + 1)]:
                schedules_dictionary["CAPITAN"] = table_data_without_header[(a + 2)]
                schedules_dictionary["CREW"] = table_data_without_header[(a + 3)]
                schedules_dictionary["AIRCRAFT"] = table_data_without_header[(a + 4)]
                schedules_dictionary["MODULE"] = table_data_without_header[(a + 5)]
                schedules_dictionary["EXCERCISE"] = table_data_without_header[(a + 6)]
                schedules_dictionary["DESCRIPTION"] = table_data_without_header[(a + 7)]
                schedules_dictionary["FLY_TYPE"] = table_data_without_header[(a + 8)]

        return jsonify({'Return': schedules_dictionary})
    

def hi(name):
    a = fta(name)
    if len(name) < 4:
        return jsonify({"ERROR": "Invalid Alias: length 4"})

    last_retun = a.http_get()
    last_retun = a.parse_html(last_retun)
    return last_retun 

@app.route("/<string:alias>")
def hello(alias):
    if alias == "favicon.ico":
        return jsonify({"ERROR": "Requested - Favicon"})
    #return hi(alias) 
    return "HI {}".format(alias)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
    

