import requests
import urllib.request
from bs4 import BeautifulSoup

DragonRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/DragonRoute/"
PoweltonSpringGardenRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/PoweltonSpringGardenRoute/"
QueenLaneRouteUrl = "https://drexel.edu/facilities/transportation/busServiceSchedules/QueenLaneRoute/"

def pushToDb(data):
    print()

def comparison(data):
    print()

def constructShape(data):
    print()

def getData(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    allTrTags = soup.findAll('tr')
    constructShape(allTrTags)

if __name__ == "__main__":
    getData(DragonRouteUrl)
    #getData(PoweltonSpringGardenRouteUrl)
    #getData(QueenLaneRouteUrl)

