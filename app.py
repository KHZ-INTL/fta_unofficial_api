#!/bin/python3

"""Unofficial FTA API for fetching flight schedules."""

import datetime
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request


class fta():

    def __init__(self, alias):
        self.alias = alias

    def get(self):
        last_return = self.request_data()
        last_return = self.parse_data(last_return)
        
        return last_return

    def format_date(self, data, method):
        """Format date/time string to and from iso standard
        This function is mainly used to format date before inserting into to the data base
        Arguments:
            data {string} -- [date/time string]
            method {string} -- [the value of string is used to decide wether convert data (date/time string) into iso or %d/%m/%YT:%H:%M:%S]
        Returns:
            date -- dateTime object"""

        if method == "iso":
            date = datetime.datetime.strptime(data, "%d/%m/%y %H:%M").isoformat()
            return date
        elif method == "display":
            date = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
        
        return date


    def request_data(self):
        """Get raw data from FTA online schedules portal website using Requests
        Alias variable is used as login credential when requesting student schedules
        Returns:
            raw_schedule -- return html data from get request
        """
        user_id = {
            'rdUsername': str(self.alias),
            'rdFormLogon': 'True',
            'rdPassword': str(self.alias),
            'Submit1': 'Logon'}
        raw_schedule = requests.post(
            'http://202.158.223.244/OPS_STUDENT_REPORTS/rdPage.aspx', data=user_id)

        if raw_schedule.status_code != 200:
            return raw_schedule.status_code
        
        return raw_schedule


    def parse_data(self, data):

        """Parse raw html data (data) using BeautifulSoup into a dictionary
        Arguments:
            data {html} -- the result of GET request for student schedules
        Returns:
            in_vars -- dictionary which contains schedule information
        """

        day = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATUARDAY", "SUNDAY"]
        rem = ["Time", "Captain", "Crew", "Aircraft", "Module", "Exercise", "Description", "Fly Type"]
        in_vars = {"DATE": "", "CAPITAN": "", "CREW": "", "AIRCRAFT": "", "MODULE": "", "EXCERCISE": "", "DESCRIPTION": "", "FLY_TYPE": ""}
        row = []
        rowb = []
        index = []

        soup = BeautifulSoup(data.text, 'html.parser')
        table_rows = soup.find("table").find_all("tr")

        for tr in table_rows:
            td = tr.find_all('td')
            [row.append(i.text) for i in td]

        for i in row:
            if i in rem or i == "":
                continue
            else:
                rowb.append(i)

        for i in rowb:
            for d in day:
                if d in str(i):
                    index.append((rowb.index(i)))

        for a in index:
            date_time = rowb[a].split("-", 2)[1].replace(" ", "")
            date_time = date_time + " " + rowb[a + 1]
            in_vars["DATE"] = str(self.format_date(date_time, "iso"))

            if ":" in rowb[(a + 1)]:
                in_vars["CAPITAN"] = rowb[(a + 2)]
                in_vars["CREW"] = rowb[(a + 3)]
                in_vars["AIRCRAFT"] = rowb[(a + 4)]
                in_vars["MODULE"] = rowb[(a + 5)]
                in_vars["EXCERCISE"] = rowb[(a + 6)]
                in_vars["DESCRIPTION"] = rowb[(a + 7)]
                in_vars["FLY_TYPE"] = rowb[(a + 8)]

        print("\n\n")

        print("{}\n\n".format(in_vars))


        return jsonify({'retunr': in_vars})


app = Flask(__name__)

@app.route('/', methods=['GET'])
def ret_none():
    return "HI"

@app.route('/api/<string:alias>', methods=['GET'])
def get_schedules(alias):
    schedules = ""
    if len(alias) > 4:
        schedules = fta(alias)
        schedules.get()
    else:
        schedules = "alias not > 4"
    return schedules

if __name__ == '__main__':
    app.run(debug=True, port=8080)
