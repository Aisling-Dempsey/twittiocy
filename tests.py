import unittest
import server



class Testcase(unittest.TestCase):

    def setUp(self):
        tweet = server.get_tweet('hackbright')
        tweets = server.build_tweets(tweet)
        hts = server.make_hts(tweets)


    def test_get_tweet(self):
        func = server.get_tweet('hackbright')
        self.assertTrue(hasattr(func, '__iter__') and not hasattr(func, '__len__'))

    def test_build_tweets(self):
        tweet = server.get_tweet('hackbright')
        func = server.build_tweets(tweet)
        self.assertEqual(type(func), list)
        self.assertEqual(type(func[0]), dict)
        self.assertTrue(func[0].get('text'))

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
        self.assertEqual(type(func), list)
        self.assertEqual(type(func[0]), tuple)




if __name__ == "__main__":
    unittest.main()