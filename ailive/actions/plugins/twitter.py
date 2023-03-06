"""
This module defines the Twitter class, which is used to interact with Twitter.
"""

import os

import logbook
import tweepy

from ailive.actions.plugins.base import AlivePlugin

_logger = logbook.Logger(__name__)

# Twitter API credentials
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY", "")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET", "")
access_key = os.environ.get("TWITTER_ACCESS_KEY", "")
access_secret = os.environ.get("TWITTER_ACCESS_SECRET", "")

# Twitter API credentials
if not consumer_key or not consumer_secret or not access_key or not access_secret:
    _logger.warn("Twitter API credentials are not set")
else:
    # Twitter API credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)


class AliveTwitterPluginMock(AlivePlugin):
    def get_notifications(self):
        return [
            "new follower: @user1",
            "dave liked your tweet: @user2",
            "user Hana Bar tagged you in a photo",
        ]

    def execute(self, tasks):
        return [
            "executed task: like a tweet",
            "executed task: follow a user",
            "executed task: retweet a tweet",
        ]
