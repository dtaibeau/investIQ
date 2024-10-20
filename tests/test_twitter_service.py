import os
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def authenticate_with_bearer_token():
    """Authenticate with Twitter API v2 using Bearer Token."""
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
        print("Authentication successful with Bearer Token!")
        return client
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def fetch_tweets_by_user(username, count=5):
    """Fetch recent tweets from a specific user using Twitter API v2."""
    client = authenticate_with_bearer_token()
    if not client:
        return []

    try:
        # Search for recent tweets from the user's timeline using the v2 endpoint
        response = client.get_users_tweets(
            id=username,
            max_results=count,
            tweet_fields=['created_at', 'text']
        )

        if response.data:
            tweets = [{"created_at": tweet.created_at, "text": tweet.text} for tweet in response.data]
            print(f"Retrieved {len(tweets)} tweets.")
            return tweets
        else:
            print("No tweets found for the specified user.")
            return []
    except tweepy.errors.Forbidden:
        print("Access Forbidden - Check your API access level and permissions.")
        return []
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

if __name__ == '__main__':
    tweets = fetch_tweets_by_user("KiteVC", count=5)
    for tweet in tweets:
        print(tweet)
