import datetime as dt
import json
import sqlite3
import time as t
from sqlite3 import Error

import numpy as np

from database import binance_getter


def write(config):
    # Loading config file

    # Used to connect to the sql database
    # This is no the file itself but a connection to it allowing for easy R/W
    def create_connection():
        # connecting to :memory: will make a database in memory
        try:
            conn = sqlite3.connect('database/binance.db')
            # print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            return conn

    def strip_interval(interval):
        if interval[-1] == 'm':
            return int(interval[0:-1])

    # Creating conn and cursor objects for writing sql
    conn = create_connection()
    c = conn.cursor()

    interval_td = config['limit'] * \
        dt.timedelta(minutes=strip_interval(config['interval']))

    # Getting data from the binance getter module which makes get requests to the binance kline endpoint
    time = dt.datetime.strptime(config['start'], '%Y-%m-%d %H:%M')
    iterations = 0
    while iterations < config['iterations']:
        
        response = binance_getter.klines(
            config['symbol'], config['interval'], time, limit=config['limit'])

        if response.data == False:
            print('breaking')
            break
        
        print(time)
        # if_exists argument can take fail, replace or append strings
        if iterations == 0:
            response.DataFrame.to_sql('coin', conn, if_exists='replace')
        else:
            response.DataFrame.to_sql('coin', conn, if_exists='append')
        time = time + interval_td
        iterations += 1

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
