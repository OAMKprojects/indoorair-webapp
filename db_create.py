from datetime import datetime, timedelta
import sqlite3
import random

entries = 500

conn = sqlite3.connect('database.db')
conn.execute("CREATE TABLE IF NOT EXISTS indoorair"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT"
                ", temperature DECIMAL(3, 1)"
                ", humidity DECIMAL(3, 1)"
                ", time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);").fetchall()

temp = 25
hum = 30
min_max_temp = [15, 40]
min_max_hum = [15, 70]

for i in range(entries):
    rand_num = random.randint(0, 5)
    if rand_num == 0:
        temp += 1
    elif rand_num == 1:
        temp -= 1
    if temp < min_max_temp[0]:
        temp = min_max_temp[0]
    elif temp > min_max_temp[1]:
        temp = min_max_temp[1]

    rand_num = random.randint(0, 5)
    if rand_num == 0:
        hum += 1
    elif rand_num == 1:
        hum -= 1
    if hum < min_max_hum[0]:
        hum = min_max_hum[0]
    elif hum > min_max_hum[1]:
        hum = min_max_hum[1]

    time_stamp = datetime.now().replace(microsecond=0) - timedelta(minutes=i*5)
    conn.execute("INSERT INTO indoorair(temperature, humidity, time) VALUES(?, ?, ?);", \
                (temp, hum, time_stamp))

result = conn.execute("SELECT * FROM indoorair ORDER BY time;").fetchall()

conn.commit()
conn.close()