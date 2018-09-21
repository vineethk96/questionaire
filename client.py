#!/usr/bin/env python3

import sys
import tweepy
import socket
import pickle
import hashlib

import argparse

from ClientKeys import *        # keys imported

from tweepy import Stream
from tweepy.streaming import StreamListener
from cryptography.fernet import Fernet
from hashlib import md5

#Format of Question:
#   "#ECE4564T18 Question Asked?"
#   "Question Asked? #ECE4564T18"
#   "#Question ECE4564T18 Asked?"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-brg", dest="bridge_ip")
    parser.add_argument("-p", dest="bridge_port")
    parser.add_argument("-z", dest="socket_size")
    parser.add_argument("-t", dest="hashtag")

    return parser.parse_args()

# ** Create a StreamListener  **
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        get_tweet(status)

    def on_error(self, status_code):
        if status_code == 403:
            print("request was understood, but refused")
            return false

# sends payload to the bridge
def clientToBridge(payload):
    """
    client socket
    """
    pickledVar = pickle.dumps(payload)      # pickle the payload

    print(pickledVar)
    print(bridgeIP)
    print(port)
    print(size)

    host = bridgeIP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host,port))
    s.send(pickledVar)
    data=s.recv(size)
    s.close()
    print('Recieved:', data)

# returns the MD5 hash for the encrypted token
def MD5_Hash(token, encoding='utf-8'):
    return md5(token.encode(encoding)).hexdigest()

# returns the dictionary containing the key and the encrypted token
def fernetEncrypt(curr_tweet):
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(curr_tweet)
    fernetDict = {'key' : key, 'token' : token}
    return fernetDict

# strips the current tweet encrypts the token and preps payload for launch
def get_tweet(tweet):
    
    curr_tweet = tweet.text
    
    # Tweet formatted to not include the hashtag anymore
    curr_tweet = curr_tweet.replace(hashtag, "")
    curr_tweet = curr_tweet.replace("  ", " ")
    print(curr_tweet)

    # Encryption
    fernetDict = fernetEncrypt(curr_tweet)
    MD5Hash = MD5_Hash(fernetDict['token'])

    # prep payload for launch
    payload = {'crypt_key': fernetDict['key'], 'text': fernetDict['token'], 'md5_hash': MD5Hash}
    clientToBridge(payload)


if __name__ == "__main__":
    #gives us secure access to the twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    if len(sys.argv) > 1:
        args = parse_args()    # decode the desired bridge ip
        bridgeIP = args.bridge_ip
        port = args.bridge_port
        size = args.socket_size
        hashtag = args.hashtag
    else:
        print("INPUT ERROR HAS OCCURED")

    # ** Create the stream **
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)


    # ** Start the stream **
    myStream.filter(track=[hashtag])

