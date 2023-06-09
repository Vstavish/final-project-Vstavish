from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from datetime import datetime, timedelta
import json
import csv

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Handle the form submission
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = sqlite3.connect('inspections.db')
        if len(search_query) == 5 and search_query.isdigit():
            # Search by zip code
            query = """
            SELECT establishment_id, name, COUNT(*) AS count, zip, owner
            FROM inspections
            WHERE zip = ?
            GROUP BY establishment_id
            ORDER BY count DESC
            """
            cursor = conn.execute(query, (search_query,))

        elif len(search_query) == 4 and search_query.isdigit():
            # Search by establishment ID
            query = """
            SELECT establishment_id, name, COUNT(*) AS count, zip, owner
            FROM inspections
            WHERE establishment_id = ?
            GROUP BY establishment_id
            """
            cursor = conn.execute(query, (search_query,))
        else:
            # Search by name or owner
            query = """
            SELECT establishment_id, name, COUNT(*) AS count, zip, owner
            FROM inspections
            WHERE name LIKE ?
            OR owner LIKE ?
            GROUP BY establishment_id
            ORDER BY count DESC
            """
            cursor = conn.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
        
        search_results = cursor.fetchall()
        conn.close()
        
        has_search_results = len(search_query) > 0 and len(search_results) > 0
        
        return render_template('index.html', search_query=search_query, search_results=search_results, has_search_results=has_search_results)
    
    else:
        # Show the default index page
        conn = sqlite3.connect('inspections.db')
        # Calculate the date 60 days ago from today
        past_date = datetime.now() - timedelta(days=60)
        past_date_str = past_date.strftime('%Y-%m-%d')

        # Retrieve the top 10 restaurants with the most critical violations in the past 60 days
        top_restaurants_query = """
        SELECT establishment_id, name, COUNT(*) AS count, zip, owner
        FROM inspections
        WHERE inspection_results LIKE '%critical violations observed%'
        AND inspection_date >= ?
        GROUP BY establishment_id
        HAVING COUNT(*) >= 1
        ORDER BY count DESC
        LIMIT 10;
        """
        top_restaurants_cursor = conn.execute(top_restaurants_query, (past_date_str,))
        top_restaurants = top_restaurants_cursor.fetchall()

        # Retrieve all establishment IDs with 1 or more critical violations in the past 60 days
        establishments_query = """
        SELECT DISTINCT establishment_id
        FROM inspections
        WHERE inspection_results LIKE '%critical violations observed%'
        AND inspection_date >= ?
        """
        establishments_cursor = conn.execute(establishments_query, (past_date_str,))
        establishment_ids = [row[0] for row in establishments_cursor.fetchall()]

        conn.close()

        # Initialize search_results with an empty list
        search_results = []

        return render_template('index.html', rows=top_restaurants, num_restaurants=len(top_restaurants), num_establishments=len(establishment_ids), time_frame=past_date_str, search_results=search_results)



@app.route("/establishment/<establishment_id>")
def establishment(establishment_id):
    conn = sqlite3.connect('inspections.db')
    # Retrieve all rows with the given establishment ID from the database
    query = """
    SELECT name, category, inspection_date, inspection_results, zip, address_line_1, owner
    FROM inspections
    WHERE establishment_id = ?
    ORDER BY inspection_date DESC
    """
    cursor = conn.execute(query, (establishment_id,))
    rows = cursor.fetchall()
    conn.close()
    if len(rows) == 0:
        # Redirect the user to the index page if the establishment ID is not found
        return redirect("/")
    else:
        # Render a template with the establishment information in a table
        name, category, _, _, zip_code, address, owner = rows[0]
        num_inspections = len(rows)
        num_critical_violations = sum('critical violations observed' in r[3].lower() for r in rows)
        num_compliant = sum('compliant - no health risk' in r[3].lower() for r in rows)
        num_non_compliant = sum('non-compliant - violations observed' in r[3].lower() for r in rows)
        num_outstanding = sum('compliance schedule - outstanding' in r[3].lower() for r in rows)
        num_completed = sum('compliance schedule - completed' in r[3].lower() for r in rows)
        null_results = sum('----' in r[3].lower() for r in rows)
        num_closed = sum('facility closed' in r[3].lower() for r in rows)
        num_reopened = sum('facility reopened' in r[3].lower() for r in rows)
        num_compliant_health_risk = sum('compliant - health risk' in r[3].lower() for r in rows)
        num_no_critical_violations = sum('no critical violations observed' in r[3].lower() for r in rows)
        return render_template('establishment.html', establishment_id=establishment_id, name=name, category=category, rows=rows, zip_code=zip_code, address=address, owner=owner, num_inspections=num_inspections, num_critical_violations=num_critical_violations, num_compliant=num_compliant, num_non_compliant=num_non_compliant, null_results=null_results, num_outstanding=num_outstanding, num_completed=num_completed, num_no_critical_violations=num_no_critical_violations, num_compliant_health_risk=num_compliant_health_risk, num_reopened=num_reopened, num_closed=num_closed)

@app.route("/violations")
def violations():
    conn = sqlite3.connect('inspections.db')
    # Retrieve all restaurants with 1 or more critical violations in the past 60 days
    query = """
    SELECT establishment_id, name, COUNT(*) AS count, zip, owner
    FROM inspections
    WHERE inspection_results LIKE '%critical violations observed%'
    AND inspection_date >= ?
    GROUP BY establishment_id
    HAVING COUNT(*) >= 1
    ORDER BY establishment_id;
    """
    past_date = datetime.now() - timedelta(days=60)
    past_date_str = past_date.strftime('%Y-%m-%d')
    cursor = conn.execute(query, (past_date_str,))
    rows = cursor.fetchall()
    conn.close()
    return render_template('violations.html', rows=rows)

@app.route("/about")
def about():
    conn = sqlite3.connect('inspections.db')
    return render_template('about.html')

@app.route("/timeline")
def timeline():
    return render_template('timeline.html')

@app.route('/data')
def data():
    conn = sqlite3.connect('inspections.db')
    cursor = conn.cursor()
    query = """
        SELECT establishment_id, name, category, inspection_date, inspection_results, zip, address_line_1, owner
        FROM inspections
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return render_template('data.html', data=data)

@app.route("/download")
def download():
    # Path to the inspections.db file
    db_file_path = "inspections.db"
    
    # Open a connection to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Execute a query to fetch the data from the inspections table
    query = "SELECT * FROM inspections"
    cursor.execute(query)
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Create a temporary file to store the CSV data
    temp_file = "temp_data.csv"

    # Write the data to the temporary CSV file
    with open(temp_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # Return the temporary CSV file as a response for download
    return send_file(temp_file, as_attachment=True, download_name="inspections.csv", mimetype="text/csv")


if __name__ == "__main__":
    app.run(debug=True, port=8000)






