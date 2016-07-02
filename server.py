from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from datetime import datetime
import tweepy
# import os

app = Flask(__name__)

# makes jinja throw error if requesting undefined value
app.jinja_env.undefined = StrictUndefined


# this is terrible practice and in reality, API keys should be sourced in through environmental vars or a similarly
# secure process

consumer_key = 'bfMdk2m22f29bbo4EAVaREqTN'
consumer_secret = 'FqQZQ7gXIO2UXuiSNsAfKEpXxpzPsrLMBulGRZTBj274Udm0ms'
access_token = '748642641223385089-kqsibOsL2Wn0FgBoVzadW3ENMgdIPyB'
access_token_secret = 'NvHHjCUGMqCIP8qbGQ54AK5SEVCBgM7ad8MmW4Upxh5OL'
SECRET_KEY = 'q;qwisad90asdjek4ie9dd9#FASDFJ'


# secure example, getting vars from a sourced secrets.sh
#
# consumer_key = os.environ['CONSUMER_KEY']
# consumer_secret = os.environ['CONSUMER_SECRET']
# access_token = os.environ['ACCESS_TOKEN']
# access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
# SECRET_KEY = os.environ['SECRET_KEY']

app.secret_key = SECRET_KEY

@app.route('/')
def splash():
    return render_template('base.html')


@app.route('/results/<int:offset>')
def get_more_results(offset):
    query = request.args.get('term')
    tweet = get_tweet(query)
    skip_to_place(offset, tweet)
    tweets = build_tweets(tweet)
    hashtags = sorted_hashtags(make_hts(tweets))
    final = last_page(tweets)
    return render_template('results.html',
                           tweets=tweets,
                           hashtags=hashtags,
                           final=final,
                           offset=offset,
                           query=query)



#########helper functions########

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure=True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_tweet(query):
    """takes search query and returns twitter object"""
    t = api.search(q=query, count=15000)
    for p in t:
        yield p


def build_tweets(t):
    """constructs array of 25 tweets (less if fewer than 25 left) from tweet generator"""
    tweets = []
    while len(tweets) < 25:
        try:
            tweet = next(t)
            tweet_info = {
                'created_at': tweet.created_at.strftime("%B %d, %Y - %I:%M %p "),
                'hashtags': tweet.entities['hashtags'],
                'text': tweet.text,
                'name': tweet.user.name,
                'screen_name': tweet.user.screen_name,
                'fave_count': tweet.favorite_count
            }
            tweets.append(tweet_info)
        except StopIteration:
            break
    return tweets

#     created_at --- datetime.datetime
#     entities['hashtags'] --- array
#     favorite_count ---  int
#     text --- str
#     user.name --- str
#     user.screen_name --- str
#     user.in_reply_to_screen_name ---str


def make_hts(tweets):
    """takes result of query and builds list of all hashtags in result."""
    hts = []
    for tweet in tweets:
        for ht in tweet['hashtags']:
            hts.append(ht['text'])
    return hts


def sorted_hashtags(hts):
    """takes hashtag array and builds descending sorted list of hashtags and how often they appear as tuples."""
    d = {}
    # builds dict of hashtags and their count
    for ht in hts:
        d[ht] = d.get(ht, 0) + 1

    return sorted(d.items(), key=lambda k: k[1], reverse=True)


def skip_to_place(offset, tweet):
    """takes offset integer and skips appropriate number of tweets. Returns generator at appropriate place."""
    to_skip = (offset-1) * 25
    # iterates through tweet generator until appropriate offset is reached, skipping tweets that have been seen before
    # May be better/more efficient way to do this, but can't find
    # offset option within API docs. Since using a generator at least memory usage is efficient.
    while to_skip > 0:
        next(tweet)
        to_skip -= 1
    return tweet


def last_page(tweets):
    """check if last page of tweets and returns boolean"""
    if len(tweets) > 24:
        return False
    else:
        return True


if __name__ == '__main__':
    # toggles debug mode on
    # app.debug = True

    # runs debug toolbar
    DebugToolbarExtension(app)

    app.run()
