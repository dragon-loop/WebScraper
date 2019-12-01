import requests
import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

DragonRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/DragonRoute/"
PoweltonSpringGardenRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/PoweltonSpringGardenRoute/"
QueenLaneRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/QueenLaneRoute/"

def pushToDb(data):
    print()

def comparison(data):
    print()

def constructShape(data, name):
    with open(name + '.json','w') as outfile:
        json.dump(data, outfile)

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
    #getData(PoweltonSpringGardenRouteUrl)
    #getData(QueenLaneRouteUrl)

