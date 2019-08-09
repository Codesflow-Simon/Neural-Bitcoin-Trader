import json
import sys
from getopt import getopt

from database.sqlite_writer import write
from train.train import prep_data, train


def opt_to_dict(opt):
    d = {}
    for pair in opt:
        d[pair[0].strip('-')] = pair[1]
    return d


opt = getopt(sys.argv[1:], 'tw', ['config='])[0]
d = opt_to_dict(opt)
if 'w' in d:
    print('writing...')
    
    with open('config.json') as config_file:
        config = json.load(config_file)['data']

    write(config)

if 't' in d:
    # Hyperparamers and settings
    with open('config.json') as config_file:
        hyperparameters = json.load(config_file)['train']

    print('preping...')
    # Getting data
    x, y, df = prep_data(hyperparameters)

    print('training...')
    # Training algorithm
    train(x, y, hyperparameters, df)
