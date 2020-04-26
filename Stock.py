import random
import time
import sqlite3
import datetime
from datetime import datetime

default = [5000000, 2000000, 2000000, 1000000, 1000000, 500000, 100000, 50000, 20000, 10000]


while True:
    now = datetime.now()
    if now.second == 0 and now.minute % 5 == 0:
        conn = sqlite3.connect("Money.db")
        cur = conn.cursor()
        for i in range(4, 14):
            for row in cur.execute('SELECT * FROM Stock WHERE name = {}'.format(i)):
                now_value = int(row[1])
                if now_value >= default[i-4]:
                    if random.randint(1, 100) <= 40:
                        change = float(random.randint(0, 10000)) ** 0.25 / 100
                    else:
                        change = float(- 1 + 1 / (1 + (float(random.randint(0, 10000)) ** 0.25) / 100))
                else:
                    if random.randint(1, 100) <= 60:
                        change = float(random.randint(0, 10000)) ** 0.25 / 100
                    else:
                        change = float(- 1 + 1 / (1 + (float(random.randint(0, 10000)) ** 0.25) / 100))
                cur.execute(
                    'UPDATE Stock SET value = {} WHERE name = {}'.format(int(now_value + int(now_value * change)), i))
                cur.execute('UPDATE Stock SET switch = {} WHERE name = {}'.format(int(now_value * change), i))
                if now.hour == 5 and now.minute == 0:
                    cur.execute('DELETE FROM {}'.format(i))
                cur.execute('INSERT INTO "{}" VALUES ({},{})'.format(str(i), int(now_value + now_value * change),
                                                                     int(now_value * change)))
        conn.commit()
        conn.close()
        print("Yes")
        if 2 <= now.hour < 7:
            time.sleep(3590)
        elif 7 <= now.hour < 9:
            time.sleep(1790)
        elif 9 <= now.hour < 20:
            time.sleep(590)
        elif 20 <= now.hour < 24:
            time.sleep(290)
        elif 0 <= now.hour < 2 or now.hour == 24:
            time.sleep(590)
