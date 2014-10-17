import json
import os

from tweepy import StreamListener
import re


def add_html(tweets):
    for tweet in tweets:
        tweet['html'] = tweet_html(tweet)

    return tweets


def ireplace(subject, search_string, replacement):
    """Find and replace, ignoring case"""

    pattern = re.compile(search_string, re.IGNORECASE)
    return pattern.sub(replacement, subject)


def create_file_and_directories(filename):
    # Create directories if necessary
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    # Touch the file
    with open(filename, "a"):
        os.utime(filename, None)


def tweet_html(tweet):
    tweet_html = tweet['text']

    for mention in tweet['entities']['user_mentions']:
        user = mention['screen_name']
        user_link = u'<a href="https://twitter.com/{0}">@{0}</a>'

        tweet_html = ireplace(
            subject=tweet_html,
            search_string='@' + user,
            replacement=user_link.format(user)
        )

    for hashtag_item in tweet['entities']['hashtags']:
        hashtag = hashtag_item['text']
        hash_link = u'<a href="https://twitter.com/hashtag/{0}">#{0}</a>'

        tweet_html = ireplace(
            subject=tweet_html,
            search_string='#' + hashtag,
            replacement=hash_link.format(hashtag)
        )

    for url_item in tweet['entities']['urls']:
        tweet_html = ireplace(
            subject=tweet_html,
            search_string=url_item['url'],
            replacement=u'<a href="{0}">{1}</a>'.format(
                url_item['url'],
                url_item['display_url']
            )
        )

    return tweet_html


class TweetStreamer(StreamListener):
    """
    A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, tweet_manager, *args, **kwargs):
        self.tweet_manager = tweet_manager

        # Call parent __init__
        super(StreamListener, self).__init__(*args, **kwargs)

    def on_data(self, data):
        tweet = json.loads(data)

        self.tweet_manager.add_tweets([tweet])

        return True


class TweetManager:
    def __init__(self, filename, max_tweets=3):
        self.filename = filename
        self.max_tweets = max_tweets

        create_file_and_directories(filename)

    def add_tweets(self, tweets):
        """Tweets come in newest first"""

        self._update_tweets_from_file()
        self.tweets = tweets + self.tweets  # Prepend new tweets
        self._write_tweets()

    def get_tweets(self):
        self._update_tweets_from_file()

        return self.tweets

    # Private methods
    def _update_tweets_from_file(self):
        file_size = os.stat(self.filename)[6]

        if file_size == 0:
            self.tweets = []
        else:
            with open(self.filename) as tweets_file:
                self.tweets = json.load(tweets_file)

        self._write_tweets()

    def _write_tweets(self):
        """Save tweets in the tweets file in JSON."""

        # Discard tweets over max_tweets
        self.tweets = self.tweets[:self.max_tweets]

        with open(self.filename, 'w') as tweets_file:
            json.dump(
                self.tweets,
                tweets_file,
                indent=4
            )
