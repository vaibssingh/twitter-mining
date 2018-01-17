import json
import operator
import re
import string
from collections import Counter, defaultdict

import tweepy
import vincent
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tweepy import OAuthHandler

#Using OAuth interface to authorize our app to access Twitter
consumer_key = "qKgqkgL14FOygq41iejwwkdvi"
consumer_secret = "PgbqHNTMQvBB6pVvsDRFJqxJqv3jcR49JygMUpUaRQB8cUJ0la"
access_token = "166564853-F9sSz9LI3TddGslool07Hsjah0Kw6rTT4fdxuJn7"
access_secret = "oMC6oHIbiMLk0G9Lg499F1Q2qe7dSs1PniYjRyMTs6lI0"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# The api variable is now our entry point for most of the operations we can perform with Twitter.
api = tweepy.API(auth)

#To continuously gather tweets about a topic or #hashtag we use streaming API StreamListener()
from tweepy import Stream
from tweepy.streaming import StreamListener


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('lohri.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#HappyLohri'])
