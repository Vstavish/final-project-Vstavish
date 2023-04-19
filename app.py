import requests
from bs4 import BeautifulSoup
import time
import urllib.request
from pprint import pprint
import csv
import os
import json

url = "https://data.princegeorgescountymd.gov/Health/Food-Inspection/umjn-t2iz"
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table element
table = soup.find("table")

# Check if the table was found
if table is None:
    print("Could not find table")
else:
    # Find all the rows in the table
    rows = table.find_all("tr")

    # Loop over the rows and print out the data in each cell
    for row in rows:
        cells = row.find_all("td")
        for cell in cells:
            print(cell.text.strip(), end="\t")
        print()