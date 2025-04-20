# Part of libunn, view: https://github.com/juanvel4000/libunn
import time
import datetime

def unix():
    return time.time()

def unn():
    unn_epoch = datetime.datetime(2025, 1, 1, 0, 0, 0)
    delta = datetime.datetime.now() - unn_epoch 
    return int(delta.total_seconds())