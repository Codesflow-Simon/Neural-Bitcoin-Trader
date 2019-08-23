import pandas as pd
import sqlite3
from sqlite3 import Error
import numpy as np


class environment:
    index = 0

    def create_connection(self, path):
        # connecting to :memory: will make a database in memory
        try:
            conn = sqlite3.connect(path)
        except Error as e:
            print(e)
        finally:
            return conn

    def minmax(self, x):
        Min = min(x)
        Max = max(x)
        z = x
        if Min==Max:
            for i, _ in enumerate(x):
                z[i] = 0.5
        else:
            for i, _ in enumerate(x):
                z[i] = (x[i]-Min)/(Max-Min)
        return z 

    def __init__ (self, length, max):
        # import database
        conn = self.create_connection('database/binance.db')
        c = conn.cursor()

        # Get data from database
        c.execute('SELECT * FROM coin')
        # Data in pandas
        df = pd.DataFrame(c.fetchall())
        df.columns = list(map(lambda x: x[0], c.description))
        del df['index'], df['open_time'], df['close_time'], df['ignore']
        print(df.index)

        # Building x
        delays = [0, 1, 2]
        _max = max(delays)
        x = []
        diff = []
        # Using df as a base to build a np array
        for i, j in df.iterrows():
            if i < _max:
                continue

            step = []
            for delay in delays:
                step.append(list(df.iloc[i-delay]))
            step = pd.DataFrame(step, columns=df.columns)
            diff.append(step.iloc[0]['c']-step.iloc[0]['o'])
            for column in step.columns:
                step[column] = self.minmax(step[column])
            x.append(step.values.flatten())
            self.x = np.array(x)
            self.diff = np.array(diff)
        # return np.array(x), np.array(diff)

    def save(self):
        self.x.save('env_np/x.npy')
        self.diff.save('env_np/d.npy')

    def reset(self):
        self.index = 0
        x = self.x[self.index]
        diff = self.diff[self.index]
        self.index += 1
        return x.reshape(-1, 27), diff


    def next_step(self):
        x = self.x[self.index]
        diff = self.diff[self.index]
        self.index += 1
        return x.reshape(-1, 27), diff
    