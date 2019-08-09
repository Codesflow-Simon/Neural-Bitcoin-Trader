from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras as k
import pandas as pd


def build_layers(model, size):
    i = 1
    while i < len(size)+1:
        if i != len(size):
            model.add(k.layers.Dense(
                size[i], activation=activation, input_shape=[size[i-1], ]))
        else:
            model.add(k.layers.Dense(
                1, activation='linear', input_shape=[size[i-1], ]))
        i += 1

def train_model(x, y, model, hyperparam):
    # Test for high verobse
    if hyperparam['verbose'] >= 1:
        if hyperparam['verbose'] >= 2:

            # Print summary
            model.summary()

        # Train model with '.' callback
        return model.fit(
            x[0:hyperparam['train_end']
            ], y[0:hyperparam['train_end']],
            epochs=hyperparam['epoch'], verbose=0, batch_size=hyperparam['batch_size'],
            callbacks=[PrintDot()])
    else:
        # Train model silently
        return model.fit(
            x[0:hyperparam['train_end']
            ], y[0:hyperparam['train_end']],
            epochs=hyperparam['epoch'], verbose=0, batch_size=hyperparam['batch_size'])

class PrintDot(k.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            print('')
        print('.', end='')

def plot_history(history, model, x, y, df):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.scatter(hist['epoch'], hist['mean_absolute_error'],
                label='Train Error', s=1)
    # plt.ylim([0, 1000])
    plt.yscale('log')
    plt.legend()

    # print(10 ** model.predict(x))

    plt.figure(figsize=(12, 8))
    try:
        plt.plot((10 ** x['c']).values, label='Price')
    except:
        plt.plot(df['c'].values, label='Price')
    plt.plot((10 ** model.predict(x)), label='Model')
    plt.plot((10 ** y).values, label='Target')

    cdict = {1: 'red', 2: 'blue', 3: 'green'}

    # plt.ylim(125, 20000)
    # plt.xlim(1100, 2200)
    plt.yscale('log')
    plt.ylabel('PriceUSD')
    plt.xlabel('Time')

    plt.legend()
    plt.show()

def activation(x):
    return k.activations.selu(x)
