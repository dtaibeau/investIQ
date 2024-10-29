import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


def authenticate_twitter():
    """Authenticate with Twitter API v1.1 using Tweepy."""
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    return client


def fetch_tweets_from_user(username, count=10):
    """Fetch tweets from a specific user."""
    client = authenticate_twitter()
    tweets_data = []

    try:
        # fetch user ID from username
        user = client.get_user(username=username)
        user_id = user.data.id

        # fetch recent tweets from user
        tweets = client.get_users_tweets(user_id, max_results=count)

        if tweets.data:
            for tweet in tweets.data:
                tweet_info = {
                    "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                    "text": tweet.text,
                }
                tweets_data.append(tweet_info)
        else:
            print("No tweets found for the specified user.")

    except Exception as e:
        print(f"Error fetching tweets: {e}")

    return tweets_data


if __name__ == '__main__':
    tweets = fetch_tweets_from_user("KiteVC", count=10)
    print(tweets)
