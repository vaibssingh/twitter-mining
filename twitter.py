import tweepy
import json
import re
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

#For example, read our own timeline
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)

#To contiously gather tweets about a topic or #hashtag we use streaming API StreamListener()
from tweepy import Stream
from tweepy.streaming import StreamListener


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('sense.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#Sense8'])

#Text pre-processing part
#Let us have a look at our collected data

with open('mytweets.json', 'r') as f:
    line = f.readline()  # read only the first tweet/line
    tweet = json.loads(line)  # load it as Python dict
    print(json.dumps(tweet, indent=4))  # pretty-print
