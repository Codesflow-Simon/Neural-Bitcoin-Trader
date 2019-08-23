import json
import sys
from getopt import getopt

from database.sqlite_writer import write
from train.dataset import x_get
from matplotlib import pyplot as plt

def opt_to_dict(opt):
    d = {}
    for pair in opt:
        d[pair[0].strip('-')] = pair[1]
    return d


opt = getopt(sys.argv[1:], 'twp', ['config='])[0]
d = opt_to_dict(opt)
if 'w' in d:
    print('writing...')

    with open(d['config']+'.json') as config_file:
        config = json.load(config_file)['data']

    write(config)

if 't' in d:
    x = x_get(None)

if 'p' in d:
    pass