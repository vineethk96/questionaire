#!/usr/bin/env python3

import datetime

def print_checkpoint(msg):
    ''' Prints a checkpoint
    Prints a timestamp and the provided message.
    '''
    time = datetime.datetime.now().time()
    hour = '{0}'.format(str(time.hour).zfill(2))
    minute = '{0}'.format(str(time.minute).zfill(2))
    second = '{0}'.format(str(time.second).zfill(2))
    time_format = '[' + hour + ':' + minute + ':' + second + ']'
    print(time_format, msg)


