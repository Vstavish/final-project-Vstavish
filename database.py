import requests
import json
import sqlite3

# Connect to a sql database called inspections.db
conn = sqlite3.connect('inspections.db')
cursor = conn.cursor()

# create a table that will hold the data scraped from the website
create_table_sql = """
CREATE TABLE inspections (
    establishment_id VARCHAR(255),
    name VARCHAR(255),
    category VARCHAR(255),
    inspection_date DATE,
    inspection_results VARCHAR(255),
    zip VARCHAR(255),
    address_line_1 VARCHAR(255),
    owner VARCHAR(255) NULL
)
"""
cursor.execute(create_table_sql)

# pull the data from the website. I'm using ?$order=inspection_date DESC to make the output chronological and I'm using  for no particular reason but that is what signifies how many rows to pull from the API
url = "https://data.princegeorgescountymd.gov/resource/umjn-t2iz.json?$limit=50000&$where=inspection_date>'2016-05-06T00:00:00.000'"

response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)
# Here I'm giving a heads up which columns I'd like to grab. Right now I'm just grabbing basic information, but once I understand the database more I plan to also pull the columns that detail exactly which type of violation a restauarant did/didn't have. That will be an additional ~16 rows unfortunately lol
    for row in data:
        try:
            owner = row['owner']
        except KeyError:
            owner = None

        try:
            zip_code = row['zip']
        except KeyError:
            zip_code = None

        try:
            address_line_1 = row['address_line_1']
        except KeyError:
            address_line_1 = None

        print(row["establishment_id"], row["name"], row["category"], row["inspection_date"], row["inspection_results"], zip_code, address_line_1, owner)

        # insert each row of pulled data into the database
        insert_sql = """
        INSERT INTO inspections
        (establishment_id, name, category, inspection_date, inspection_results, zip, address_line_1, owner)
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
    row["establishment_id"],
    row["name"].lower(),
    row["category"].lower(),
    row["inspection_date"],
    row["inspection_results"].lower(),
    zip_code.lower() if zip_code else zip_code,
    address_line_1.lower() if address_line_1 else address_line_1,
    owner.lower() if owner else owner
)
        cursor.execute(insert_sql, values)
    
    # commit these changes to the database
    conn.commit()
    print(f"Inserted {len(data)} rows into the database.")
else:
    print("Failed to retrieve data")

# close the connection to the database
conn.close()
