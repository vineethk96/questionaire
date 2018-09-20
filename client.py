#!/usr/bin/env python3

import sys
import tweepy
import ClientKeys
from optparse import OptionParser

from ClientKeys import *        # keys imported

#Format of Question:
#   "#ECE4564T18 Question Asked?"
#   "Question Asked? #ECE4564T18"
#   "#Question ECE4564T18 Asked?"

print("consumer key: ")
print(consumer_key)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
        print tweet.text
