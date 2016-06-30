from flask import Flask, render_template, request
import tweepy

app = Flask(__name__)

# this is terrible practice and in reality, API keys should be sourced in through environmental vars or a similarly
# secure process

consumer_key = 'bfMdk2m22f29bbo4EAVaREqTN'
consumer_secret = 'FqQZQ7gXIO2UXuiSNsAfKEpXxpzPsrLMBulGRZTBj274Udm0ms'
access_token = '748642641223385089-kqsibOsL2Wn0FgBoVzadW3ENMgdIPyB'
access_token_secret = 'NvHHjCUGMqCIP8qbGQ54AK5SEVCBgM7ad8MmW4Upxh5OL'





@app.route('/')
def splash():
    return render_template(splash.html)

@app.route('/results')
def display_query():
    query = request.args.get('query')




#########helper functions########

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure=True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



def get_tweets(query):
    """takes search query and returns twitter object"""
    return api.search(q=query)

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
    # builds dict of hastags and their count
    for ht in hts:
        d[ht] = d.get(ht, 0) + 1

    return sorted(d.items(), key=lambda k: k[1], reverse=True)


if __name__ == '__main__':
    app.run()
