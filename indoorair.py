from flask import Flask, render_template, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def update_db():
    conn = get_db_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS indoorair"
                 "(id INTEGER PRIMARY KEY AUTOINCREMENT"
                 ", temperature DECIMAL(3, 1)"
                 ", humidity DECIMAL(3, 1)"
                 ", time ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP);").fetchall()

    for i in range(10):
        conn.execute("INSERT INTO indoorair(temperature, humidity) VALUES(?, ?);", (i, i + 10))

    conn.commit()
    conn.close()

def load_db():
    conn = get_db_connection()
    result = conn.execute("SELECT * FROM indoorair;").fetchall()

    conn.close()
    return result

@app.route('/')
def index():
    dbvalues = load_db()
    return render_template("index.html", posts = dbvalues)

@app.route('/24h')
def history():
    dbvalues = load_db()
    return render_template("24h.html", posts = dbvalues)

if __name__ == '__main__':
    #update_db()
    app.run(debug=True)