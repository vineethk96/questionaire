#!/usr/bin/env python3

import sys
from optparse import OptionParser

from ServerKeys import wolfram_alpha_app_id
from lib import print_checkpoint

def parse_args(args):
    ''' Parse command-line arguments and returns dictionary of arguments
    '''
    parser = OptionParser()
    parser.add_option("-p", dest="server_port", help="server PORT", metavar="PORT")
    parser.add_option("-b", dest="backlog_size", help="backlog SIZE", metavar="SIZE")
    parser.add_option("-z", dest="socket_size", help="socket SIZE", metavar="SIZE")

    return parser.parse_args()

if __name__ == "__main__":
    opts, args = parse_args(sys.argv[1:])
    print(opts)
    print_checkpoint("Hello")

