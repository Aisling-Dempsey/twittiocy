import unittest
import server


class Testcase(unittest.TestCase):

    def test_get_tweet(self):
        func = server.get_tweet('hackbright')
        self.assertTrue(hasattr(func, '__iter__') and not hasattr(func, '__len__'))

    def test_build_tweets(self):
        tweet = server.get_tweet('hackbright')
        func = server.build_tweets(tweet)
        self.assertIsInstance(func, list)
        self.assertIsInstance(func[0], dict)
        self.assertTrue(func[0].get('text'))
        self.assertIsInstance(func[0]['text'], unicode)

    def test_make_hts(self):
        tweet = server.get_tweet('hackbright')
        tweets = server.build_tweets(tweet)
        func = server.make_hts(tweets)
        self.assertEqual(type(func), list)

    def test_sorted_hashtags(self):
        tweet = server.get_tweet('hackbright')
        tweets = server.build_tweets(tweet)
        hts = server.make_hts(tweets)
        func = server.sorted_hashtags(hts)
        self.assertIsInstance(func, list)
        self.assertIsInstance(func[0], tuple)

    def test_strip_links(self):
        tweet = server.get_tweet('hackbright')
        tweets = server.build_tweets(tweet)
        func=server.strip_links(tweets)
        self.assertIsInstance(func[0]['text'], list)
        self.assertIsInstance(func[0]['text'][0], tuple)


if __name__ == "__main__":
    unittest.main()