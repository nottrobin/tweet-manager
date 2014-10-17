Tweet manager
===

A class and scripts for managing a JSON file of tweet data from a specific user account. The default location of the JSON file is `data/tweets.json`.

This uses [Tweepy](https://github.com/tweepy/tweepy) to consume data from the [REST](https://dev.twitter.com/rest/public) and [Streaming](https://dev.twitter.com/streaming/overview) Twitter APIs v1.1.

Settings
---

Before using this you need to update `settings.py` with the ID of a Twitter user, and some API credentials.

You can get the ID for a Twitter user from <http://gettwitterid.com/>, and you should be able to create API credentials by visiting <https://apps.twitter.com/>.

``` python
# settings.py

settings = {
    # The ID number for a twitter user - see http://gettwitterid.com/
    'user_id': '{user-id}',

    # API authentication credentials
    'consumer_key': '{api-consumer-key}',
    'consumer_secret': '{api-consumer-secret}',
    'access_token': '{api-access-token}',
    'access_token_secret': '{api-access-token-secret}',

    ...
```

Scripts
---

There are two scripts you can use to retrieve and watch for tweets:

### get-tweets.py

``` bash
$ ./get-tweets.py 
Updating data/tweets.json with the top 3 tweets from https://twitter.com/intent/user?user_id=xxxxxxx
Done
```

This will use [the REST API](https://dev.twitter.com/rest/public) to get the top tweets from the set Twitter account and store them in the tweets file (`data/tweets.json` by default). `max_tweets`, `user_id` and `tweets_filename` can be updated in `settings.py`.

### stream-tweets.py

``` bash
$ ./stream-tweets.py 
Listening for tweets from https://twitter.com/intent/user?user_id=xxxxxxx (ctrl+c to exit)...
```

This will use [the Streaming API](https://dev.twitter.com/streaming/overview) to listen for any new tweets to the set Twitter account, and add them to the tweets file (`data/tweets.json` by default). The number of tweets stored in the file will never exceed the `max_tweets` setting.

TweetManager
---

The `TweetManager` class in `models.py` can be used to manage a JSON file of tweets, to read tweets or add to them:

``` python
# Specify your own options
tweet_manager = TweetManager(
    filename='my-tweets.json',
    max_tweets=10
)

# Or use the existing settings
from settings import settings
manager = TweetManager(
    settings['tweets_filename'], int(settings['max_tweets'])
)

# To get tweets from the file
tweets =  manager.get_tweets()

# Or add tweets to the file
more_tweets = []  # Populate this with tweet data
manager.add_tweets(more_tweets)
```

Tests
---

You can test that the models work okay with [Pytest](http://pytest.org/latest/):

```bash
$ py.test
```
