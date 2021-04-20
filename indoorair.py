from flask import Flask, render_template, url_for, jsonify, request
from datetime import datetime
import json
import sqlite3
import random

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

    for i in range(24):
        time_stamp = datetime(2021, 4, 17, i, 0, 0)
        conn.execute("INSERT INTO indoorair(temperature, humidity, time) VALUES(?, ?, ?);", \
                    (random.randint(10, 30), random.randint(15, 70), time_stamp))

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

def get_text_and_pic(temp, hum):
    data = [
        ['static/too_hot_and_wet.txt', 'bgimg_too_hot'],
        ['static/too_cold.txt', 'bgimg_too_cold'],
        ['static/too_dry.txt', 'bgimg_too_dry'],
        ['static/perfect.txt', 'bgimg_perfect']
    ]

    if temp > 26:
        val = 0
    elif temp < 18:
        val = 1
    elif hum < 25:
        val = 2
    else:
        val = 3

    with open(data[val][0], "r", encoding="utf-8") as file:
        text = file.read()
        image = data[val][1]
        return text, image

@app.route('/load_db_val', methods=['POST'])
def load_db_val():
    data = request.get_json(force=True)
    datatype = data['datatype']
    conn = get_db_connection()
    #result = conn.execute("SELECT " + datatype + ", strftime('%H', time) as minute FROM indoorair ORDER BY time;").fetchall()
    result = conn.execute("SELECT " + datatype + ", time as minute FROM indoorair WHERE datetime(time) >= datetime('now', '-3 hour') ORDER BY time;").fetchall()
    conn.close()

    ret_val = []
    list_th = list(result)
    for val in list_th:
        ret_val.append({ 'y' : val[datatype], 'x' : val['minute']})

    return jsonify({datatype : ret_val})

@app.route('/temp_chart')
def temp_chart():
    return render_template("chart_temp.html")

@app.route('/hum_chart')
def hum_chart():
    return render_template("chart_hum.html")

@app.route('/reload_db', methods=['GET'])
def reload_db():
    conn = get_db_connection()
    result = conn.execute("SELECT temperature,humidity FROM indoorair ORDER BY id DESC LIMIT 1;").fetchall()
    conn.close()

    list_th = list(result[0])
    temp = list_th[0]
    hum = list_th[1]
    text, image = get_text_and_pic(temp, hum)

    return jsonify({"temperature" : temp, "humidity" : hum, "text" : text, "image" : image})

@app.route('/')
def index():
    #update_db()
    tem_values = load_temp()
    hum_values = load_hum()
    text, image = get_text_and_pic(24, 30)
    return render_template("index.html", content = text, temps = tem_values, humis = hum_values, image_class = image)

@app.route('/24h') 
def history():
    dbvalues = load_db()
    return render_template("24h.html", posts = dbvalues)

if __name__ == '__main__':
    app.run(debug=True)