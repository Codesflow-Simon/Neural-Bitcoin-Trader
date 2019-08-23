import datetime as dt
import json
import sqlite3
from datetime import timedelta
from sqlite3 import Error

with open('config.json') as config_file:
    config = json.load(config_file)

# Used to connect to the sql database
# This is no the file itself but a connection to it allowing for easy R/W
class query_database():
    def unix_time_millis(self, datetime_object):
        return (datetime_object - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000

    def create_connection(self):
        # connecting to :memory: will make a database in memory
        try:
            conn = sqlite3.connect('database/binance.db')
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            return conn

    def convert_to_timedelta(self, time_val):
        num = int(time_val[:-1])
        if time_val.endswith('s'):
            return timedelta(seconds=num)
        elif time_val.endswith('m'):
            return timedelta(minutes=num)
        elif time_val.endswith('h'):
            return timedelta(hours=num)
        elif time_val.endswith('d'):
            return timedelta(days=num)

    def __init__(self, date):
        if type(date) == str:
            date_time = dt.datetime.strptime(date, '%d/%m/%Y %H:%M')
        conn = self.create_connection()
        c = conn.cursor()
        window_open = int(self.unix_time_millis(date_time))
        window_close = int(self.unix_time_millis((date_time-self.convert_to_timedelta(config['interval']))))
        # print(window_open, type(window_open))
        # print(window_close, type(window_close))
        c.execute('SELECT close_time FROM coin')
        # print(c.fetchall())
        c.execute("SELECT * FROM coin WHERE close_time <= " + str(window_open) + " AND close_time > " + str(window_close))

        # print(list(map(lambda x: x[0], c.description)))
    
        
        # c.execute("SELECT time FROM coin")
        self.data = c.fetchall()


print(query_database('01/07/2019 00:10').data)
