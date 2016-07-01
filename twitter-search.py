from flask import Flask, render_template, request
import tweepy
import os


app = Flask(__name__)

# this is terrible practice and in reality, API keys should be sourced in through environmental vars or a similarly
# secure process

consumer_key = 'bfMdk2m22f29bbo4EAVaREqTN'
consumer_secret = 'FqQZQ7gXIO2UXuiSNsAfKEpXxpzPsrLMBulGRZTBj274Udm0ms'
access_token = '748642641223385089-kqsibOsL2Wn0FgBoVzadW3ENMgdIPyB'
access_token_secret = 'NvHHjCUGMqCIP8qbGQ54AK5SEVCBgM7ad8MmW4Upxh5OL'

# secure example, getting vars from a sourced secrets.sh
#
# consumer_key = os.environ['CONSUMER_KEY']
# consumer_secret = os.environ['CONSUMER_SECRET']
# access_token = os.environ['ACCESS_TOKEN']
# access_token_secret = os.environ['ACCESS_TOKEN_SECRET']


@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/results/<offset>')
def get_more_results(offset):
    query = request.args.get('query')
    tweet = get_tweet(query)

    # skips tweets that have been seen before. May be better/more efficient way to do this, but can't find
    # offset option within API docs. Using a generator at least memory usage is efficient.
    skip_to_place(offset, tweet)
    tweets = build_tweets(tweet)
    hashtags = sorted_hashtags(make_hts(tweets))
    final = last_page(tweets)
    return render_template('results.html',
                           tweets=tweets,
                           hashtags=hashtags,
                           final=final,
                           offset=offset)



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
            tweets.append(next(t))
        except StopIteration:
            break
    return tweets


def make_hts(tweets):
    """takes result of query and builds list of all hashtags in result."""
    hts = []
    for tweet in tweets:
        for ht in tweet.entities['hashtags']:
            hts.append(ht['text'])
    return hts


def sorted_hashtags(hts):
    """takes hastag iterable and builds descending sorted list of hashtags and how often they appear."""
    d = {}
    # builds dict of hashtags and their count
    for ht in hts:
        d[ht] = d.get(ht, 0) + 1

    return sorted(d.items(), key=lambda k: k[1], reverse=True)


def skip_to_place (offset, tweet):
    """takes offset integer and skips appropriate number of tweets. Returns generator at appropriate place."""
    to_skip = (offset-1) * 25
    while to_skip > 0:
        next(tweet)
        to_skip -= 1
    return tweet


def last_page(tweets):
    """check if last page of tweets"""
    if len(tweets) > 24:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run()
