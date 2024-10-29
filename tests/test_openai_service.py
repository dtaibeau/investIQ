import unittest
from app.services.twitter_service import fetch_tweets_from_user
from app.services.openai_service import generate_ai_summary


class TestOpenAISummaryService(unittest.TestCase):

    def setUp(self):
        """Set up the test case by fetching real tweets from Bill Tai."""
        self.tweets = fetch_tweets_from_user("KiteVC", count=10)

    def test_generate_summary_with_real_tweets(self):
        """Test generating AI summary using real tweets."""
        if not self.tweets:
            self.fail("Failed to fetch real tweets for testing.")

        summary = generate_ai_summary(self.tweets)

        if summary:
            print("\nAI Summary of Bill Tai's Recent Tweets:\n")
            print(summary)
            self.assertIn("Trend:", summary)
            self.assertIn("Investment Opportunities:", summary)
        else:
            self.fail("Failed to generate AI summary.")


if __name__ == '__main__':
    unittest.main()
