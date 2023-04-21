import requests
import json
import sqlite3

# establish a connection to the database
conn = sqlite3.connect('inspections.db')
cursor = conn.cursor()

# create a table to hold the data
create_table_sql = """
CREATE TABLE inspections (
    establishment_id VARCHAR(255),
    name VARCHAR(255),
    category VARCHAR(255),
    inspection_date DATE,
    inspection_results VARCHAR(255),
    zip VARCHAR(255),
    address_line_1 VARCHAR(255)
)
"""

url = "https://data.princegeorgescountymd.gov/resource/umjn-t2iz.json?$order=inspection_date DESC&$limit=2000"

response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)
    for row in data:
        print(row["establishment_id"], row["name"], row["category"], row["inspection_date"], row["inspection_results"], row["zip"], row["address_line_1"])
else:
    print("Failed to retrieve data")