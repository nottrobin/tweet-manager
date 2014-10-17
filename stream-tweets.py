#!/usr/bin/env python

from tweepy import Stream

from models import TweetStreamer
from twitter_setup import (
    auth,
    manager,
    user_id
)

streamer = TweetStreamer(manager)

# Set streamer to follow tweets
print (
    "Listening for tweets from "
    "https://twitter.com/intent/user?user_id={0} "
    "(ctrl+c to exit)..."
).format(user_id)

stream = Stream(auth, streamer)
stream.filter(follow=[user_id])
