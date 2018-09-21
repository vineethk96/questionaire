#!/usr/bin/env python3

import sys
from optparse import OptionParser
import socket
import pickle
import hashlib
from cryptography.fernet import Fernet
import wolframalpha

from ServerKeys import wolfram_alpha_app_id
from lib import print_checkpoint


def get_answer(question):
    ''' API call to create and return the answer payload for the given
        question.'''
    client = wolframalpha.Client(wolfram_alpha_app_id)
    print_checkpoint("Sending question to Wolframalpha: " + question)
    results = client.query(question)
    if results["@success"] == "false":
        answer = "Question could not be resolved"
    else:
        subpod = results['pod'][1]['subpod']
        if isinstance(subpod, list):
            answer = subpod[0]['plaintext']
        else:
            answer = subpod['plaintext']
    print_checkpoint("Received answer from Wolframalpha: " + answer)
    return answer


class Server:
    ''' This server object manages the socket connection withe the bridge and 
        the communication with the Wolfram Alpha engine.'''
    def __init__(self, server_port, backlog_size, socket_size):
        ''' Initializes the socket connection with the bridge.'''
        self.server_port = int(server_port)
        self.backlog_size = int(backlog_size)
        self.socket_size = int(socket_size)
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', self.server_port))
        print_checkpoint("Created socket at 0.0.0.0 on port "
                         + server_port)
        self.listener.listen(self.backlog_size)
        print_checkpoint("Listening for client connections")
        self.bridge, address = self.listener.accept()
        bridge_address = str(address[0])
        bridge_port = str(address[1])
        print_checkpoint("Accepted client connection from "
                         + bridge_address + " on port " + bridge_port)
    
    def answer_questions(self):
        ''' Waits until a question payload is received over the socket, 
            answers the question and sends the answer payload back.'''
        data = self.bridge.recv(self.socket_size)
        if not data:
            raise socket.error("No data received")
        data = pickle.loads(data)
        print_checkpoint("Received data: " + str(data))
        m = hashlib.md5()
        m.update(data["text"])
        if m.hexdigest() != data["md5_hash"]:
            raise ValueError("MD5 checksums on the encrypted question did"
                             + " not match")
        key = data["crypt_key"]
        crypt_tool = Fernet(key)
        question = crypt_tool.decrypt(data["text"]).decode()
        print_checkpoint("Decrypt: Key: " + key.decode() + " | Plaintext "
                         + question)
        answer = get_answer(question)
        encrypted_answer = crypt_tool.encrypt(str.encode(answer))
        print_checkpoint("Encrypt: Key: " + key.decode() + " | Ciphertext "
                         + encrypted_answer.decode())
        m.update(encrypted_answer)
        md5_checksum = m.hexdigest()
        print_checkpoint("Generated MD5 Checksum: " + md5_checksum)
        payload = {"text" : encrypted_answer, "md5_hash" : md5_checksum}
        serialized_payload = pickle.dumps(payload)
        print_checkpoint("Sending data: " + str(serialized_payload))
        self.bridge.send(serialized_payload)

    def __del__(self):
        ''' Closes the socket connections.'''
        if hasattr(self, 'listener'):
            self.listener.close()
        if hasattr(self, 'bridge'):
            self.bridge.close()


def parse_args(args):
    ''' Parse command-line arguments and returns dictionary of arguments.'''
    parser = OptionParser()
    parser.add_option("-p", dest="server_port", help="server PORT",
                      metavar="PORT")
    parser.add_option("-b", dest="backlog_size", help="backlog SIZE",
                      metavar="SIZE")
    parser.add_option("-z", dest="socket_size", help="socket SIZE", 
                      metavar="SIZE")

    return parser.parse_args()

if __name__ == "__main__":
    opts, args = parse_args(sys.argv[1:])
    server = Server(opts.server_port, opts.backlog_size, opts.socket_size)
    while True:
        server.answer_questions()
