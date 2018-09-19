#!/usr/bin/env python3
import sys, socket, BridgeKeys
from optparse import OptionParser


def parse_args(args):
    parser = OptionParser()
    parser.add_option("--svr-p", dest="server_port", help="server port", metavar="SVRPORT")
    parser.add_option("--svr", dest="server_ip", help="server IP", metavar="IP")
    parser.add_option("-p", dest="bridge_port", help="bridge port", metavar="PORT")
    parser.add_option("-b", dest="backlog_size", help="backlog size", metavar="SIZE")
    parser.add_option("-z", dest="socket_size", help="socket size", metavar="SIZE")

    return parser.parse_args()

if __name__ == "__main__":
    opts, args = parse_args(sys.argv[1])
    print(opts)
    server_port = opts.server_port
    server_ip = opts.server_ip
    bridge_port = opts.bridge_port
    backlog_size = opts.backlog_size
    socket_size = opts.socket_size

    try:
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print('Failed to create sockets. Error code: ' + str(msg[0]) + ', ' + msg[1])
        sys.exit();
    sender.connect((server_ip, server_port))
    listener.bind((socket.gethostname(), bridge_port))
    listener.listen(backlog_size)
