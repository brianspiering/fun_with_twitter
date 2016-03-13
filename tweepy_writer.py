#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A simple streaming writer from Twitter's API.

Inspired by http://adilmoujahid.com/posts/2014/07/twitter-analytics/
"""

import json
import os
import sys

from credentials import credentials
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

limit = 2 # Number of tweets to save

# Load credentials from ~/.credentials.json
creds = credentials.require(['access_token', 
                             'access_token_secret', 
                             'consumer_key',
                             'consumer_secret'])

auth = OAuthHandler(creds.consumer_key, creds.consumer_secret)
auth.set_access_token(creds.access_token, creds.access_token_secret)

class WriteToDiskListener(StreamListener):
    """Write stream listener to disk with limited number of Tweets.
    """

    def __init__(self, filename, limit=5):
        self.counter = 0
        self.filename = filename
        self.limit = limit
        
    def on_data(self, data):
        "If under limit, write received data to disk."
        while self.counter < self.limit:
            try:
                with open(self.filename.lower()+'.json', 'a') as f:
                    f.write(data)
                self.counter += 1
                return True
            except BaseException as e:
                print("Error on_data: {}".format(e))
            return True
        else:
            return False
 
    def on_error(self, status):
        print(status)

if __name__ == '__main__':    
    track = sys.argv[1:] # Track is a list of search terms to stream.
    filename = "_".join([item.lower() for item in track])

    # # Remove existing file of tweets
    # try:
    #     os.remove(filename+'.json')
    # except OSError:
    #     pass

    listener = WriteToDiskListener(filename=filename, 
                                    limit=limit)
    stream = Stream(auth, listener)

    try:
        stream.filter(track=track,
                      languages=['en'])
    except:
        stream.disconnect()