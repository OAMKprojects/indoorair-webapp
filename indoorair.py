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

def load_db():
    conn = get_db_connection()
    result = conn.execute("SELECT * FROM indoorair ORDER BY id DESC;").fetchall()
    conn.close()
    return list(result[0])[0]

def load_temp(): #Haetaan viimeisin lämpötila
    conn = get_db_connection()
    result = conn.execute("SELECT temperature FROM indoorair ORDER BY id DESC LIMIT 1;").fetchall()
    conn.close()
    return list(result[0])[0]

def load_hum(): #Haetaan viimeisin kosteus
    conn = get_db_connection()
    result = conn.execute("SELECT humidity FROM indoorair ORDER BY id DESC LIMIT 1;").fetchall()
    conn.close()
    return list(result[0])[0]

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
    result = conn.execute("SELECT " + datatype + ", datetime(time, 'localtime') as time FROM indoorair WHERE time >= datetime('now', '-24 Hour') ORDER BY time;").fetchall()
    conn.close()

    ret_val = []
    list_th = list(result)
    for val in list_th:
        ret_val.append({ 'y' : val[datatype], 'x' : val['time']})

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
    tem_value = load_temp()
    hum_value = load_hum()
    text, image = get_text_and_pic(tem_value, hum_value)
    return render_template("index.html", content = text, temps = tem_value, humis = hum_value, image_class = image)

@app.route('/24h') 
def history():
    dbvalues = load_db()
    return render_template("24h.html", posts = dbvalues)

if __name__ == '__main__':
    app.run(debug=True)