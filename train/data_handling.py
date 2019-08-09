
import math
import sqlite3

import numpy as np
import pandas as pd

predict = 'c'

def log_object(data_frame):
    data_frame_two = data_frame.copy()
    for i, _ in enumerate(data_frame):
        if data_frame.iat[i] != 0:
            data_frame_two.iat[i] = math.log10(data_frame.iat[i])
    return data_frame_two


def shift_cells(price_column, sight):
    shifted = price_column.copy()
    for i, _ in enumerate(shifted):
        if i < len(shifted)-sight:
            shifted.iat[i] = shifted.iat[i+sight].copy()
        else:
            shifted.iat[i] = float('nan')
    shifted = shifted[np.isfinite(shifted)]
    shifted = log_object(shifted)
    return shifted

def create_connection():
    # connecting to :memory: will make a database in memory
    try:
        conn = sqlite3.connect('database/binance.db')
        # print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return conn

def trim(df, sight, delays=[]):
    def trim_column(item, sight):
        shifted = item.copy()
        for i, _ in enumerate(shifted):
            if i < len(shifted)-sight:
                shifted.iat[i] = shifted.iat[i].copy()
            else:
                shifted.iat[i] = float('nan')
        return shifted

    # Will remove NaN in PriceUSD
    trimmed = df.copy()
    # Removes NaNs by marking elemnts as NaN then removes all NaN's
    trimmed[predict] = trim_column(trimmed[predict], sight)
    for column in trimmed.columns:
        try:
            trimmed[column] = log_object(trimmed[column])
            trimmed = trimmed[np.isfinite(trimmed[column])]
        except TypeError:
            pass
    return trimmed
