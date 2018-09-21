#!/usr/bin/env python3

import sys
import tweepy
import socket

from optparse import OptionParser

from ClientKeys import *        # keys imported

#Format of Question:
#   "#ECE4564T18 Question Asked?"
#   "Question Asked? #ECE4564T18"
#   "#Question ECE4564T18 Asked?"

#gives us secure access to the twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

"""
# Find the most recent tweet with the hashtag
for tweet in tweepy.Cursor(api.search,q='#ECE4564T18',result_type="recent").items(1):
	print("Tweet: " + tweet.text)
	curr_tweet = tweet.text

# Tweet formatted to not include the hashtag anymore
curr_tweet = curr_tweet.replace("#ECE4564T18", "")
curr_tweet = curr_tweet.replace("  ", " ")
print(curr_tweet)
"""

import tweepy
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())

myStream.filter(track=['#ECE4564T18'])

    def on_error(self, status_code):
	if status_code == 420:
        #returning False in on_data disconnects the stream
	return False

"""
client socket
"""

"""
host = '192.168.1.108'
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send(curr_tweet)
data=s.recv(size)
s.close()
print('Recieved:', data)
"""
