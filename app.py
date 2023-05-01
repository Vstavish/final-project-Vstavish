from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect('inspections.db')
    # Define the SQL query to retrieve the establishment IDs and their counts
    query = """
    SELECT establishment_id, COUNT(*) as count, name, zip, owner
    FROM inspections
    GROUP BY establishment_id
    ORDER BY count DESC
    LIMIT 10;
    """
    # Execute the SQL query and fetch the results
    cursor = conn.execute(query)
    results = cursor.fetchall()

    # Execute the SQL query and fetch the results
    cursor = conn.execute(query)
    results = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    # Render the template with the data
    return render_template('index.html', rows=results)


    # Format the results as a response
    response = ''
    for result in results:
        response += f'{result[0]}: {result[1]}\n'
    return response


if __name__ == "__main__":
    app.run(debug=True)


