#!/bin/python3

"""Unofficial FTA API for fetching flight schedules.
"""

import datetime
import os

import requests
from bs4 import BeautifulSoup

# Insert your FTA-Alias: e.g = myname7226
alias = "anvari7126"

# Initialisations

def cls():
    """Clear Screen
    This function Clears the screen
    """
    os.system('CLEAR')

    return None

def format_date(data, method):
    """Format date/time string to and from iso standard
    This function is mainly used to format date before inserting into to the data base
    Arguments:
        data {string} -- [date/time string]
        method {string} -- [the value of string is used to decide wether convert data (date/time string) into iso or %d/%m/%YT:%H:%M:%S]
    Returns:
        date -- dateTime object
    """
    if method == "iso":
        date = datetime.datetime.strptime(data, "%d/%m/%y %H:%M").isoformat()
        return date
    elif method == "display":
        date = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
    return date


def request_data():
    """Get raw data from FTA online schedules portal website using Requests
    Alias variable is used as login credential when requesting student schedules
    Returns:
        raw_schedule -- return html data from get request
    """
    user_id = {
        'rdUsername': str(alias),
        'rdFormLogon': 'True',
        'rdPassword': str(alias),
        'Submit1': 'Logon'}
    raw_schedule = requests.post(
        'http://202.158.223.244/OPS_STUDENT_REPORTS/rdPage.aspx', data=user_id)

    if raw_schedule.status_code == 200:
        print("DEBUG: GET - OK\n")
    else:
        print("DEBUG: GET - ERROR: ",raw_schedule.status_code)

    return raw_schedule


def parse_data(data):

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
        in_vars["DATE"] = str(format_date(date_time, "iso"))

        if ":" in rowb[(a + 1)]:
            in_vars["CAPITAN"] = rowb[(a + 2)]
            in_vars["CREW"] = rowb[(a + 3)]
            in_vars["AIRCRAFT"] = rowb[(a + 4)]
            in_vars["MODULE"] = rowb[(a + 5)]
            in_vars["EXCERCISE"] = rowb[(a + 6)]
            in_vars["DESCRIPTION"] = rowb[(a + 7)]
            in_vars["FLY_TYPE"] = rowb[(a + 8)]

    return in_vars


if __name__ == "__main__":
parse_data(request_data())