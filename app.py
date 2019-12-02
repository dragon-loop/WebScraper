import requests
import urllib.request
from bs4 import BeautifulSoup
import json
from os import path
import os.path
import sys
import psycopg2

DragonRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/DragonRoute/"
PoweltonSpringGardenRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/PoweltonSpringGardenRoute/"
QueenLaneRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/QueenLaneRoute/"

def pushToDb(data, name):
    #localhost db -> currently wont connect
    #conn = psycopg2.connect("host='localhost' dbname='postgres' port='60561' user='postgres' password='password' connect_timeout=60")
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="password", port="60690")
    cur = conn.cursor()

def comparison(data, name):
    #open the file for compare
    original = open(os.path.join(sys.path[0], name + '.json'), 'r')
    originalJsonObj = json.loads(original.read())
    compareAgainstJsonObj = json.loads(data)

    a, b = json.dumps(originalJsonObj), json.dumps(compareAgainstJsonObj)
    #if not equal then push to db else dont do anything and
    if not a == b:
        pushToDb(data, name)
    else:
        return

def constructShape(data, name):
    if not path.exists(name + '.json'):
        with open(name + '.json','w') as outfile:
            json.dump(data, outfile)
        pushToDb(data)
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
        cells = row.find_all("td")
        items = {}
        for index in headers:
            items[headers[index]] = cells[index].text
        data.append(items)
    constructShape(data, name)
if __name__ == "__main__":
    pushToDb('test', "DragonRoute")
    #getData(DragonRouteUrl, "DragonRoute")
    #getData(PoweltonSpringGardenRouteUrl, "PoweltonSpringGardenRoute")
    #getData(QueenLaneRouteUrl, "QueenLaneRoute")

