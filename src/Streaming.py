import tweepy
import sqlite3

class App:
    """docstring for App."""
    def __init__(self, consumerKey, consumerSecret):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret


class User:
    """docstring for account."""
    def __init__(self, App, accessToken, accessSecret):
        self.App = App
        self.consumerKey = App.consumerKey
        self.consumerSecret = App.consumerSecret
        self.accessToken = accessToken
        self.accessSecret = accessSecret


class Streaming:
    """各アカウントでのストリーミング処理"""
    def __init__(self, User):
        self.User = User
        # TODO tweepyの認証

    @classmethod
    def start(self):
        pass
        #TODO 各ユーザの処理
