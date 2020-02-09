# WebScraper

Requirements To Run
-------------
1. pip needs to be installed
2. python3 needs to be installed
3. BeautifulSoup, bs4, requests, json, path, os.path, sys, psycopg2, datetime, and config need to be installed via pip

What Is This?
-------------
This is a simple Python application intended to web scrape against the Drexel bus schedule. It will build a JSON shape for each route and do comparison with the previous day's shape. If the shapes don't match then it will update the PostGres DB with the new schedule.

DO NOT DOs
-------------
JSON files should be in root with the app.py file. Do not move it or it will result in creating a new file.
