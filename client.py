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
from tweepy import OAuthHandler
from cryptography.fernet import Fernet
from hashlib import md5
from lib import print_checkpoint

#Format of Question:
#   "#ECE4564T18 Question Asked?"
#   "Question Asked? #ECE4564T18"
#   "#Question ECE4564T18 Asked?"

payload = {}
bridgeIP = ""
port = 0
size = 0
hashtag = ""

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
        try:
            get_tweet(status)
        except KeyError as e:
            return True

    def on_error(self, status_code):
        if status_code == 403:
            print("request was understood, but refused")
            return False

# strips the current tweet encrypts the token and preps payload for launch
def get_tweet(tweet):

    # Prepare to send to the socket
    print_checkpoint("Listening for Tweets that contain: " + hashtag)
    
    curr_tweet = tweet.text
    print_checkpoint("New Tweet: " + curr_tweet)  #checkpoint 3

    # Tweet formatted to not include the hashtag anymore
    curr_tweet = curr_tweet.replace(hashtag, "")
    curr_tweet = curr_tweet.replace("  ", " ")

    # Encryption
    key = Fernet.generate_key()    
    f = Fernet(key)
    curr_tweet_as_bytes = str.encode(curr_tweet)
    token = f.encrypt(curr_tweet_as_bytes)

    fernetDict = {'key' : key, 'token' : token}

    #checkpoint 4
    print_checkpoint("Encrypt: Generated Key: " + str(key) + " | Ciphertext: " + str(token))

    m = md5()
    m.update(fernetDict['token'])

    # prep payload for launch
    payload['crypt_key'] = fernetDict['key']
    payload['text'] = fernetDict['token']
    payload['md5_hash'] = m.hexdigest()

    pickledVar = pickle.dumps(payload)      # pickle the payload

    #checkpoint 5
    print_checkpoint("Sending data: " + str(payload))
    s.send(pickledVar)
    data=s.recv(size)
    #checkpoint 6
    print_checkpoint("Recieved data: " + str(data))

    # decrypt the payload and print to screen

    depickledDict = pickle.loads(data)
    
    encryptAns_inBytes = depickledDict['text']
    md5ans = depickledDict['md5_hash']

    m1 = md5()

    m1.update(encryptAns_inBytes)

    print(m1.hexdigest())

    if(m1.hexdigest() == md5ans):
        decryptAnsBytes = f.decrypt(encryptAns_inBytes)
        decryptAns = decryptAnsBytes.decode()

        #checkpoint 7
        print_checkpoint("Decrypt: Using Key: " + str(key) + " | Plaintext: " + decryptAns)

    else:
        print("md5 did not match")


    return True


if __name__ == "__main__":
    #gives us secure access to the twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    if len(sys.argv) > 1:
        args = parse_args()    # decode the desired bridge ip
        bridgeIP = args.bridge_ip
        port = int(args.bridge_port)
        size = int(args.socket_size)
        hashtag = args.hashtag
    else:
        print("INPUT ERROR HAS OCCURED")
        # end program

    host = bridgeIP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host,port))
    print_checkpoint("Connecting to " + bridgeIP + " on port " + str(port)) #checkpoint 1
    
    # ** Create the stream **
    myStreamListener = MyStreamListener()    
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    # ** Start the stream **
    myStream.filter(track=[hashtag])



