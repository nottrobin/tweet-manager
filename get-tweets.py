#!/usr/bin/env python

from tweepy import API
from tweepy.parsers import JSONParser

from twitter_setup import (
    auth,
    filename,
    manager,
    max_tweets,
    user_id
)

print (
    "Updating {file} with the top {max} tweets from "
    "https://twitter.com/intent/user?user_id={id}"
).format(
    max=max_tweets,
    id=user_id,
    file=filename
)

# Get initial tweets
twitter_api = API(auth)

initial_tweets = twitter_api.user_timeline(
    user_id=user_id,
    count=max_tweets,
    parser=JSONParser()
)
manager.add_tweets(initial_tweets)

print "Done"
