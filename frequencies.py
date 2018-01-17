import tweepy
from tweepy import OAuthHandler
import json

#Using OAuth interface to authorize our app to access Twitter
consumer_key = "qKgqkgL14FOygq41iejwwkdvi"
consumer_secret = "PgbqHNTMQvBB6pVvsDRFJqxJqv3jcR49JygMUpUaRQB8cUJ0la"
access_token = "166564853-F9sSz9LI3TddGslool07Hsjah0Kw6rTT4fdxuJn7"
access_secret = "oMC6oHIbiMLk0G9Lg499F1Q2qe7dSs1PniYjRyMTs6lI0"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# The api variable is now our entry point for most of the operations we can perform with Twitter.
api = tweepy.API(auth)

with open('mytweets.json', 'w') as f:
    for tweet in tweepy.Cursor(api.user_timeline).items(3881):
        f.write(json.dumps(tweet._json)+"\n")