#!/usr/bin/env python3

import datetime

def print_checkpoint(msg):
    ''' Prints a checkpoint
    Prints a timestamp and the provided message.
    '''
    time = datetime.datetime.now().time()
    hour = str(time.hour)
    minute = str(time.minute)
    second = str(time.second)
    time_format = '[' + hour + ':' + minute + ':' + second + ']'
    print(time_format, msg)


