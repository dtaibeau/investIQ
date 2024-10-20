import unittest
from app.services.twitter_service import fetch_tweets_by_trend

class TestTwitterService(unittest.TestCase):

    def test_fetch_tweets_by_trend(self):
        trend_keyword = "blockchain"
        tweets = fetch_tweets_by_trend(trend_keyword, count=5)

        self.assertIsInstance(tweets, list)
        self.assertGreater(len(tweets), 0)


if __name__ == "__main__":
    unittest.main()
