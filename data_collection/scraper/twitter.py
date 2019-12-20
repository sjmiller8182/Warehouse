"""Twitter
Basic scraping utility for Twitter, implementing the scraper abstract api.
"""


# imports
import os
import time
import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict
import logging

import tweepy

from abstract_api import AbstractAPI
from base import get_api_keys

class TwitterScraper(AbstractAPI):
    """
    A class used to pull data from Twitter, implementing the abstract api.

    Attributes
    ----------
    connection : tweepy.api
        An instance of the tweepy api wrapper
    apikeys : List[str]
        A list of API keys for Twitter [APIKey, APISecretKey]
    tokens : List[str]
        A list of access tokens for Twitter [AccessToken, AccessTokenSecret]
    path : int
        A path to the key file (keys.yaml)

    Methods
    -------
    connect()
        Establishes a connection with Twitter
    get(params)
        Runs a collection operation from Twitter
    """

    def __init__(self, path: str) -> None:
        """
        Parameters
        ----------
        path : str
            A path to the key file (keys.yaml)
        """

        self.connection = None
        self.apikeys = None
        self.tokens = None
        self.path = path

    def connect(self) -> None:
        """Creates a tweepy.API instance and authenticates with Twitter.
        """
        if (self.apikeys is None) or (self.tokens is None):
            keys = get_api_keys('twitter', self.path)
            self.apikeys = [keys['APIKey'], keys['APISecretKey']]
            self.tokens = [keys['AccessToken'], keys['AccessTokenSecret']]
        # be sure to generate from list
        auth = tweepy.OAuthHandler(*self.apikeys)
        auth.set_access_token(*self.tokens)    
        self.connection = tweepy.API(auth)   

    def _get_user_timeline(self, screen_name, items = None, item_limit: int = 0, tweet_mode="extended"):
        """Use the tweepy.API instance to get a user timeline.

        Parameters
        ----------
        screen_name : str
            The user screen name to access
        items : None
            Not implemented
        item_limit : int, optional
            A limit for the number of response. An input of 0 is ignored.
        """

        statuses = list()
        for status in tweepy.Cursor(self.connection.user_timeline,
                                    screen_name=screen_name,
                                    tweet_mode=tweet_mode).items(limit = item_limit):
            statuses.append(status)
        return statuses

    def get(self, params: Dict[str,str]):
        raise NotImplementedError