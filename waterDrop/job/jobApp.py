# condig:UTF-8
import time
from datetime import datetime
import sqlite3

if __name__ == '__main__':
    while True:
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute("select * from auth_user")
        records = c.fetchall()
        for record in records:
            print(record)
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        conn.close()
        time.sleep(1)
