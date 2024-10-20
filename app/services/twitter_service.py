import csv
import os
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")


# Load environment variables from .env
load_dotenv()

def test_twitter_v2():
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    try:
        response = client.search_recent_tweets(query="test", max_results=1)
        if response.data:
            print(f"Tweet: {response.data[0].text}")
        else:
            print("No tweets found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_twitter_v2()