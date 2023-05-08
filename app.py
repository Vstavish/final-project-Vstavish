from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle the search query
        search_query = request.form["search_query"]
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
            cursor = conn.execute(query, ('%'+search_query+'%', '%'+search_query+'%'))
        results = cursor.fetchall()
        conn.close()
        return render_template('index.html', rows=results, search_query=search_query)
    else:
        # Show the default index page
        conn = sqlite3.connect('inspections.db')
        query = """
        SELECT establishment_id, name, COUNT(*) AS count, zip, owner
        FROM inspections
        WHERE inspection_results LIKE '%critical violations observed%'
        GROUP BY establishment_id
        ORDER BY count DESC
        LIMIT 10;
        """
        cursor = conn.execute(query)
        results = cursor.fetchall()
        conn.close()
        return render_template('index.html', rows=results)

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
        return render_template('establishment.html', establishment_id=establishment_id, rows=rows)


if __name__ == "__main__":
    app.run(debug=True, port=8000)




