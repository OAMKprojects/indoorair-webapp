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
    result = conn.execute("SELECT * FROM indoorair ORDER BY id DESC;").fetchall()
    conn.close()
    return result

def load_temp(): #Haetaan viimeisin lämpötila
    conn = get_db_connection()
    result = conn.execute("SELECT temperature FROM indoorair ORDER BY id DESC LIMIT 1;").fetchall()
    conn.close()
    return result

def load_hum(): #Haetaan viimeisin kosteus
    conn = get_db_connection()
    result = conn.execute("SELECT humidity FROM indoorair ORDER BY id DESC LIMIT 1;").fetchall()
    conn.close()
    return result

@app.route('/')
def index():
    dbvalues = load_db()
    tem_values = load_temp()
    hum_values = load_hum()
    return render_template("index.html", posts = dbvalues, temps = tem_values, humis = hum_values)

@app.route('/24h') #metodi jolla haetaan tietokannan tiedot 
def history():
    dbvalues = load_db()
    return render_template("24h.html", posts = dbvalues)

if __name__ == '__main__':
    #update_db()
    app.run(debug=True)