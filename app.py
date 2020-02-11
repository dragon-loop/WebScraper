import requests
import urllib.request
from bs4 import BeautifulSoup
import json
from os import path
import os.path
import sys
import psycopg2
from datetime import datetime

DragonRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/DragonRoute/"
PoweltonSpringGardenRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/PoweltonSpringGardenRoute/"
QueenLaneRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/QueenLaneRoute/"

def pushToDb(data, name):
    routeId = 0

    if(name== "DragonRoute"):
        routeId = 1
    elif(name == "PoweltonSpringGardenRoute"):
        routeId = 2
    elif(name == "QueenLaneRoute"):
        routeId = 3

    conn = psycopg2.connect(host="50.116.63.34", database="postgres", user="admin", password="postgres_admin", port="5432")
    cur = conn.cursor()

    counterTrip = 1
    counterStop = 1
    for row in data:
        for key, value in row.items():
            #no time for this stop
            if("–" not in value and " " not in value):
                if("PM" not in value):
                    timeObj = datetime.strptime(str(value).strip(), '%I:%M%p')
                else:
                    timeObj = datetime.strptime(str(value).strip(), '%I:%M %p')
                #print(timeObj.time())
                cur.execute("insert into schedules (route_id, trip_id, stop_id, expected_time) VALUES (" + str(routeId) + ", " + str(counterTrip) + ", " + str(counterStop) + ", \'" + str(timeObj.time()) + "\')")

                counterStop+=1
        counterStop = 1
        #print("Trip: " + str(counterTrip))
        counterTrip+=1
    conn.commit()
    

def comparison(data, name):
    #open the file for compare
    original = open(os.path.join(sys.path[0], name + '.json'), 'r')
    originalJsonObj = json.loads(original.read())
    compareAgainstJsonObj = json.loads(data)

    a, b = json.dumps(originalJsonObj), json.dumps(compareAgainstJsonObj)
    #if not equal then push to db and replace existing item else dont do anything
    if not a == b:
        #pushToDb(data, name)
        os.remove(name + ".json")
        with open(name + '.json','w') as outfile:
            json.dump(data, outfile)
    else:
        return

def constructShape(data, name):
    if not path.exists(name + '.json'):
        with open(name + '.json','w') as outfile:
            json.dump(data, outfile)
        #pushToDb(data, name)
    else:
        comparison(json.dumps(data), name)

def getData(url, name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = soup.find_all("tr")
    headerTr = table.find("tr")
    columnNames = headerTr.find_all("strong")

    #create list of column headers
    headers={}
    for i in range(len(columnNames)):
        headers[i] = columnNames[i].text.strip().lower()

    #append data to headers
    data = []
    for row in rows:
        if("strong" not in row):
            cells = row.find_all("td")
            items = {}
            if(len(cells) > 0):
                counter = 0
                for index in headers:
                    if(counter < len(headers) and len(cells) == len(headers)):
                        items[headers[index]] = cells[index].text
                    counter+=1
                data.append(items)

    #remove first index as that are column headers
    data.pop(0)
    constructShape(data, name)
if __name__ == "__main__":
    getData(DragonRouteUrl, "DragonRoute")
    getData(PoweltonSpringGardenRouteUrl, "PoweltonSpringGardenRoute")
    getData(QueenLaneRouteUrl, "QueenLaneRoute")

