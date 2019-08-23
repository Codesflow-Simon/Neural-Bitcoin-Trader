
import math
import sqlite3
from sqlite3 import Error

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd

pipe_main = Pipeline([
    ('normalization', StandardScaler())
])


def shifter(column, sight, top):
    if top:
        column = column[column.index < len(column) - sight]
    else:
        column = column[column.index >= sight]
    return column


def y_prep(y_col, sight):
    y = y_col.copy()
    # convet to dataframe
    y_frame = y.to_frame()
    # Uses shift function
    y_shift = shifter(y_frame, sight, top=False)
    return y_shift


class add_prevs:
    def __init__(self, hyperparam):
        self.prevs = hyperparam['prevs']
        self.prevs.append(0)
        self.prevs.sort()
        self.max = max(self.prevs)

    def __column_id_gen(self, column_id, delay):
        if delay == 0:
            return column_id
        else:
            return column_id + '_' + str(delay)

    def fit(self, x, y=None):
        return x
    # Adds in columns for prev datapoints based on prevs config

    def transfrom(self, x, y=None):
        x_delay = {}
        for column in x.columns:
            for delay in self.prevs:
                # _id = self.__column_id_gen(column, delay)
                _id = delay
                x_delay[column][_i] = shifter(x[column], delay, top=True)
                x_delay[column][_id] = shifter(
                    x_delay[_id], self.max - delay, top=False)
                x_delay[column][_id] = x_delay[column][_id].reset_index(inplace=False)
                x_delay[column][_id] = x_delay[column][_id][_id[0]]

        # Adds all columns together
        return pd.concat(x_delay, axis=1)

    def fit_transform(self, x, y=None):
        X = self.fit(x)
        return self.transfrom(X)


def minmax(x, _min=0, _max=1):
    def div(x, inter):
        for i, _ in enumerate(x):
            x[i] /= inter
        return x

    def minus(x, inter):
        for i, _ in enumerate(x):
            x[i] -= inter
        return x

    arr_max = max(x)
    arr_min = min(x)

    # y = ax + b
    y = minus(x, arr_min)
    y = div(y, arr_max - arr_min)
    return y


def x_prep(df, hyperparam):
    # Will remove NaN in PriceUSD
    x = df.copy()
    # Remove unwanted x values
    del x['index'], x['open_time'], x['close_time'], x['ignore']

    # Select wanted attrubutes out of remaining
    for attribute in x:
        if not(attribute in hyperparam['attributes']):
            del x[attribute]

    x_pd = x

    # Function for generating column names
    x_prev = add_prevs(hyperparam).fit_transform(x_pd)

    x_alter = x_prev.copy()
    for row in range(len(x_prev)):
        x_alter.iloc[row] = minmax(x_prev.iloc[row])


    x_shift = shifter(x_prev, hyperparam['sight'], top=True)

    return x_shift, x_prev


def create_connection(path):
    # connecting to :memory: will make a database in memory
    try:
        conn = sqlite3.connect(path)
    except Error as e:
        print(e)
    finally:
        return conn
