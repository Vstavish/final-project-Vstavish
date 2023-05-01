from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle the search query
        search_query = request.form["search_query"]
        conn = sqlite3.connect('inspections.db')
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

if __name__ == "__main__":
    app.run(port=8000)



