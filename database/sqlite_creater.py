import binance_getter
import sqlite3
from sqlite3 import Error

# Used to connect to the sql database
# This is no the file itself but a connection to it allowing for easy R/W
def create_connection():
    # connecting to :memory: will make a database in memory
    try:
        conn = sqlite3.connect('database/binance.db')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return conn

# Creating conn and cursor objects for writing sql
conn = create_connection()
c = conn.cursor()

# Create table
try:
    c.execute("DROP TABLE coin")
except:
    c.execute("CREATE TABLE coin('open_time', 'o', 'h', 'l', 'c', 'v', 'close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore')")