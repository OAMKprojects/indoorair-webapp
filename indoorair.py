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

def print_PerfText():
    with open("static/perfect.txt", "r", encoding="utf-8") as file:
        content = file.read()
        return content

def print_ColdText():
    with open("static/too_cold.txt", "r", encoding="utf-8") as file:
        content = file.read()
        return content

def print_DryText():
    with open("static/too_dry.txt", "r", encoding="utf-8") as file:
        content = file.read()
        return content

def print_HotText():
    with open("static/too_hot_and_wet.txt", "r", encoding="utf-8") as file:
        content = file.read()
        return content

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
    tem_values = load_temp()
    hum_values = load_hum()
    teksti = print_ColdText()
    return render_template("index.html", content = teksti, temps = tem_values, humis = hum_values)

@app.route('/24h') 
def history():
    dbvalues = load_db()
    return render_template("24h.html", posts = dbvalues)

if __name__ == '__main__':
    app.run(debug=True)