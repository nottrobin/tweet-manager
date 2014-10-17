from tweepy import OAuthHandler

from models import TweetManager
from settings import settings

filename = settings['tweets_filename']
max_tweets = int(settings['max_tweets'])
user_id = settings['user_id']

# Authentication
auth = OAuthHandler(
    settings['consumer_key'],
    settings['consumer_secret']
)
auth.set_access_token(
    settings['access_token'],
    settings['access_token_secret']
)

manager = TweetManager(filename, max_tweets)
