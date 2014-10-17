import json
from os import remove, path
from shutil import copyfile

from unittest import TestCase

from models import (
    add_html,
    tweet_html,
    TweetManager
)


FIXTURES_DIR = 'data/test'


class TwitterTestCase(TestCase):
    base_filepath = path.join(FIXTURES_DIR, 'test_tweets.json')
    extra_filepath = path.join(FIXTURES_DIR, 'extra_tweets.json')
    tweets_filepath = path.join(FIXTURES_DIR, 'tweets.json')
    max_tweets = 5

    def setUp(self):
        copyfile(self.base_filepath, self.tweets_filepath)
        self.manager = TweetManager(self.tweets_filepath, self.max_tweets)

    def tearDown(self):
        remove(self.tweets_filepath)

    def test_get_tweets(self):
        # Get tweets from manager
        # This should actually crop the file to max_tweets
        manager_tweets = self.manager.get_tweets()

        # Get tweets from file
        with open(self.tweets_filepath) as tweets_file:
            tweets = json.load(tweets_file)

        # The seed file actually had 7 tweets in it initially,
        # but the manager should have cut it down to max_tweets
        self.assertEquals(len(tweets), self.max_tweets)
        self.assertEquals(tweets, manager_tweets)

    def test_add_tweets(self):
        with open(self.extra_filepath) as extra_file:
            extra_tweets = json.load(extra_file)

        initial_tweets = self.manager.get_tweets()

        # Check we have max_tweets in manager
        self.assertEquals(len(initial_tweets), self.max_tweets)

        self.manager.add_tweets(extra_tweets)

        new_tweets = self.manager.get_tweets()

        # Check tweets have changed
        self.assertNotEquals(initial_tweets, new_tweets)

        # Check extra tweets are cropped - still have max_tweets
        self.assertEquals(len(initial_tweets), self.max_tweets)

        # Check top tweet is the top new one
        self.assertEquals(new_tweets[0], extra_tweets[0])

    def test_tweet_html(self):
        # The top tweet in the tweets file is a good one to test
        test_tweet = self.manager.get_tweets()[0]
        expected_html = (
            u'<a href="https://twitter.com/hashtag/testtesttest">'
            u'#testtesttest</a> '
            u'<a href="https://twitter.com/nottRobin">@nottRobin</a> '
            u'\u2666\u2665\u2663\u2660\u2740\u273f\u2708 '
            u'<a href="https://t.co/rgYNeuT864">robinwinslow.co.uk</a>'
        )

        actual_html = tweet_html(test_tweet)

        self.assertEquals(expected_html, actual_html)

    def test_add_html(self):
        # The top tweet in the tweets file is a good one to test
        tweets = self.manager.get_tweets()
        expected_tweet = tweets[0]
        expected_tweet['html'] = (
            u'<a href="https://twitter.com/hashtag/testtesttest">'
            u'#testtesttest</a> '
            u'<a href="https://twitter.com/nottRobin">@nottRobin</a> '
            u'\u2666\u2665\u2663\u2660\u2740\u273f\u2708 '
            u'<a href="https://t.co/rgYNeuT864">robinwinslow.co.uk</a>'
        )

        updated_tweets = add_html(tweets)

        self.assertEquals(expected_tweet, updated_tweets[0])
