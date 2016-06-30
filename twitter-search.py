from flask import Flask, render_template, request
import Twitter

app = Flask(__name__)

# this is terrible practice and in reality, API keys should be sourced in through environmental vars or a similarly
# secure process




@app.route('/')
def splash():
    return render_template(splash.html)

@app.route('/results')
def display_query():
    query = request.args.get('query')



#########helper functions########

def sorted_hashtags(hts):
    """takes hastag iterable and builds descending sorted list of hashtags and how often they appear."""
    d = {}
    # builds dict of hastags and their count
    for ht in hts:
        d[ht] = d.get(ht, 0) + 1

    return sorted(d.values(), key=lambda k: k[1], reverse=True)


if __name__ == '__main__':
    app.run()
