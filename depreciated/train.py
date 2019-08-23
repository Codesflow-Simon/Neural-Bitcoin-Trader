import json
import os
import sqlite3
import time
from sqlite3 import Error

import pandas as pd
import tensorflow as tf
from tensorflow import keras as k

from train import data_handling as dh
from train import keras_functions as kf


def prep_data(hyperparam):
    # import database
    conn = dh.create_connection(hyperparam['database_path'])
    c = conn.cursor()

    # Get data from database
    c.execute('SELECT * FROM coin')
    # Data in pandas
    df = pd.DataFrame(c.fetchall())
    df.columns = list(map(lambda x: x[0], c.description))

    # Create x and y vars
    x, pre_shift = dh.x_prep(df, hyperparam)
    y = dh.y_prep(pre_shift['c'], hyperparam['sight'])
    # Calculating train_end if not provided
    if hyperparam['train_end'] == None:
        hyperparam['train_end'] = len(x)-hyperparam['test_length']
    
    return x, y, df


def train(x, y, hyperparam, df):
    for i in range(hyperparam['iters']):
        # If model exists and restart is false
        if os.path.isfile(hyperparam['model_path']) & ~hyperparam['restart']:
            # User output
            if hyperparam['verbose'] >= 2:
                print('\nFound model file\n')

            # Load existing model
            model = k.models.load_model(hyperparam['model_path'], custom_objects={
                                        'activation': kf.activation})

            if not(hyperparam['epoch'] == 0):
                # Training model
                train = kf.train_model(x, y, model, hyperparam)

                # Test performance
                model.evaluate(x[hyperparam['train_end']:hyperparam['train_end'] + hyperparam['test_length']],
                            y[hyperparam['train_end']:hyperparam['train_end'] + hyperparam['test_length']], verbose=2)

                # Save model to file
                k.models.save_model(model, hyperparam['model_path'])
                # If graph is true, graph data
                if hyperparam['graph']:
                    kf.plot_history(train, model, x, y, df)

        # If model hasnt been created
        else:
            # User output
            if hyperparam['verbose'] >= 2:
                print('\nNo save model found. Creating new\n')

            # Building model framework
            model = k.Sequential(
                [k.layers.Dense(hyperparam['size'][0], kf.activation, input_shape=[x.shape[1], ])])

            # Build layers of model based on size of model
            kf.build_layers(model, hyperparam['size'])

            # Preparing model
            model.compile(optimizer='Adamax',
                        loss='logcosh',
                        metrics=['accuracy', 'mean_absolute_error'])

            # Training model
            # Testing user output levels
            if not(hyperparam['epoch'] == 0):
                # Training model
                train = kf.train_model(x, y, model, hyperparam)

                # Test performance
                model.evaluate(x[hyperparam['train_end']:hyperparam['train_end'] + hyperparam['test_length']],
                            y[hyperparam['train_end']:hyperparam['train_end'] + hyperparam['test_length']], verbose=2)

                # save model
                k.models.save_model(model, hyperparam['model_path'])

                # If graph is true, graph data
                if hyperparam['graph']:
                    # try:
                    kf.plot_history(train, model, x, y, df)
                    # except KeyError:
                    #     pass



