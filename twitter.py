import tweepy
import json
import re
import operator
import string
from tweepy import OAuthHandler
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams
from collections import Counter

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
# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     print(status.text)

# #To contiously gather tweets about a topic or #hashtag we use streaming API StreamListener()
# from tweepy import Stream
# from tweepy.streaming import StreamListener


# class MyListener(StreamListener):

#     def on_data(self, data):
#         try:
#             with open('sense.json', 'a') as f:
#                 f.write(data)
#                 return True
#         except BaseException as e:
#             print("Error on_data: %s" % str(e))
#         return True

#     def on_error(self, status):
#         print(status)
#         return True


# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=['#Sense8'])

#Text pre-processing part
#Let us have a look at our collected data

with open('/home/the_doctor/python.json', 'r') as f:
    line = f.readline()  # read only the first tweet/line
    tweet = json.loads(line)  # load it as Python dict
    print(json.dumps(tweet, indent=4))  # pretty-print

#Writing regex rules to consider various aspects of a tweet

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')',re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$',re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]
    return tokens

#To process all our tweets, previously saved on file

with open('/home/the_doctor/python.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
        print(tokens)

#Term freq

fname = '/home/the_doctor/python.json'

#Removing the stop words as observed in the results above
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['RT', 'via', '@netflix', '…']

with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        #terms_all = [term for term in preprocess(tweet['text'])] Changed after adding the stop list
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
        # Update the counter
        count_all.update(terms_stop)
    # Print the first 5 most frequent words
    #print(count_all.most_common(5))

#Few more ways to customize the filters

# Count terms only once, equivalent to Document Frequency
terms_single = set(terms_stop)
# Count hashtags only
terms_hash = [term for term in preprocess(tweet['text'])
              if term.startswith('#')]
# Count terms only (no hashtags, no mentions)
terms_only = [term for term in preprocess(tweet['text'])
              if term not in stop and
              not term.startswith(('#', '@'))]
# mind the ((double brackets))
# startswith() takes a tuple (not a list) if
# we pass a list of inputs
terms_bigram = bigrams(terms_stop)