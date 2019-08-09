Neural Trader
Neural trader is a machine learing model built in tensorflow and keras. It is used to predict future prices in cryptocurrency markets

Getting Started
To get started using Neural Trader, clone the repository onto your machine and run app.py in python 3.7.
First you must create your database,
create a copy of config.json and edit to the "data" object:

"interval" is the interval between datapoints i.e. "5m", "2h", "1d"
"symbol" is the symbol for the market you want to download
"start" is the earliest date you want your dataset to contain (yyyy-mm-dd hh:mm)
the product of "limit" and "iterations" is the amount of datapoint you want to download
limit cannot be larger than 1000, if you want more data than 1000 points, you can increase iterations
i.e. "limit": 1000
     "iterations": 20
 will download 20,000 datapoints
it is recomened to have sleep at 0 for fastest speeds (will be removed soon)

i.e.
"data": 
     {
        "interval": "30m",
        "symbol": "BTCUSDT",
        "start": "2019-08-08 00:00",
        "limit": 1000,
        "iterations": 1000,
        "sleep": 0
    }
    
Once your database is created it needs to be trained
to train your model first edit the "train" object in config.json 

TRAINING
Next your model need to be trained, edit the "train" object in config.json
"model_path" (str) is the path to where your model file will save
"restart" (bool) is wheither it will override model file if it exists
"graph" (bool) is wheither graphs will be shown to user of training process
"iters" (int) will loop training (recomended 1, will be removed soon)
"sleep" (int) (recomened 0, will be removed soon)

"epoch" (int) number of training epoch
"train_end" (null or int) will make train on only the first x samples
"test_length" (int) number of datapoint that will be saved for testing
"batch_size" (int) number of datapoints per training batch
"size" (array of int), the number on nodes per hidden layer (excluding input layer, including final layer)
"sight" (int) the number of intervals in the future that the algorithm will try to predict the price
"attributes" (array of str) what data is used, can be:
                                          "o" for open (first trade of interval)
                                          "h" for high (most expensive trade of interval)
                                          "l" for low (cheapest trade of interval)
                                          "c" for close (most recent trade of interval)
                                          "v" for volume (sum asset value of trades in interval)
                                          "qav" for Quote asset volume (sum currency value of trade in interval)
                                          "num_trades" number of trades
                                          "taker_base_vol" taker buy base volume (volume when the buyer crossess the spread in currency)
                                          "taker_quote_vol" take quote volume (volume when the buyer crossess the spread in assets)
i.e.
"train": 
     {
        "model_path": "models/model.h5",
        "restart": false,
        "verbose": 2,
        "graph": false,
        "iters": 1,
        "sleep": 5,
        "epoch": 1,
        "train_end": null,
        "test_length": 5000,
        "batch_size": 32,
        "size": [1],
        "sight": 5,
        "attributes": ["c", "v"]
    }
run app.py with flag -t (for train) and specify config.
i.e. >python app.py -t --config example.json

Prerequisites
built-ins:
    json, sqlite3, time, sys, getopt, os
pip packages:
    datetime, numpy, tensorflow, pandas(windows), urllib3, certifi
apt packages (linux)
    python-pandas

Installing
clone repository, see getting started to see how to build a database

Built With
Python

Contributing
Please submitt a pull requests to us.

Versioning
We use SemVer for versioning. For the versions available, see the tags on this repository.

Authors
Simon Littel
See also the list of contributors who participated in this project.

License
Yet to be licenced
