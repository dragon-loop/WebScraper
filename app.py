import requests
import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from os import path
import os.path
import sys

DragonRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/DragonRoute/"
PoweltonSpringGardenRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/PoweltonSpringGardenRoute/"
QueenLaneRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/QueenLaneRoute/"

def pushToDb(data, name):
    print()

def comparison(data, name):
    #open the file for compare
    original = open(os.path.join(sys.path[0], name + '.json'), 'r')
    originalJsonObj = json.loads(original.read())
    compareAgainstJsonObj = json.loads(data)

    a, b = json.dumps(originalJsonObj), json.dumps(compareAgainstJsonObj)
    if not a == b:
        pushToDb(data, name)

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
    getData(DragonRouteUrl, "DragonRoute")
    #getData(PoweltonSpringGardenRouteUrl, "PoweltonSpringGardenRoute")
    #getData(QueenLaneRouteUrl, "QueenLaneRoute")

