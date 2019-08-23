import datetime as dt
import json
import sys
import numpy as np

import certifi
import pandas as pd
import urllib3

# Create urllib3 pool manager to make requests
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
# Base of the url to be making requests to
base_url = 'https://api.binance.com/api/v1/'
# The endpoint we will be making requests to
endpoint = 'klines'
# Secret key
secret = 'dfeWl70m5lcXSDJaY5H5izBT8PNIK6tCnRQyS3RTJexQB3VYMOEjMiNgKSz4IyR7'.encode(
    'UTF8')

# The base class for making requests to the base url
# note: this only works for klines


class get_data:
    # Making requests
    def request(self, url, request='GET', use_key='false'):
        # Do or do not use api key for making requests
        if use_key:
            r = http.request(request, url, headers={
                             'X-MBX-APIKEY': '2nEB2Lj5W2bNt3iLPqBVezaz4vYSyqY8vm771MVyK1FeRpzUBdQ107PT1MjQtvZZ'})
        else:
            r = http.request(request, url)
        # Loads json recieved as dictionary
        data = json.loads(r.data)
        del r
        # Converts recieved data to DataFrame
        df = pd.DataFrame(data)
        # Heading the DataFrame
        try:
            df.columns = ['open_time',
                        'o', 'h', 'l', 'c', 'v',
                        'close_time', 'qav', 'num_trades',
                        'taker_base_vol', 'taker_quote_vol', 'ignore']
            # Converting strings to floats
            self.data = True
            return df.apply(pd.to_numeric, errors='coerce')

        except(ValueError):
            self.data = False
            return df


    # Converts datetime to milliseconds since epoch
    def unix_time_millis(self, datetime_object):
        return (datetime_object - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000

    # converts time as dd/mm/yyyy hh:mm to milliseconds since epoch
    def convert_time(self, data):
        if (type(data['startTime']) == str):
            data['startTime'] = int(self.unix_time_millis(
                dt.datetime.strptime(data['startTime'], '%Y-%m-%d %H:%M')))
        else: 
            data['startTime'] =int(self.unix_time_millis(data['startTime']))
        if (type(data['endTime']) == str):
            data['endTime'] = int(self.unix_time_millis(
                dt.datetime.strptime(data['endTime'], '%Y/%m/%d %H:%M')))
        else:
            data['endTime'] = int(self.unix_time_millis(data['endTime']))
        return data

    # Joins url base and query together
    def join_url(self, base, data):
        return base + '?' + self.create_string_query(data)

    # Converts object to query string
    def create_string_query(self, data):
        string = ''
        for point in data:
            if string != '' and isinstance(point, str):
                string = string + '&' + point + '=' + str(data[point])
            elif string == '' and isinstance(point, str):
                string = point + '=' + str(data[point])
            elif string != '' and isinstance(point, bytes):
                string = string + '&' + point + '=' + \
                    str(data[point].decode('UTF8'))
        return string

# Creates an instance fo get_data


class klines(get_data):
    # Recieves infomation about the request
    def __init__(self, symbol, interval, startTime, endTime=dt.datetime.now(), limit=1000):
        self.data = self.convert_time({
            'symbol': symbol,
            'interval': interval,
            'startTime': startTime,
            'endTime': endTime,
            'limit': limit
        })
        self.url = self.join_url(base_url + endpoint, self.data)
        # Makes request
        self.DataFrame = self.request(self.url)


# data = klines('BTCUSDT', '5m', '01/07/2019 00:00')
# print(data.response.values[2])
