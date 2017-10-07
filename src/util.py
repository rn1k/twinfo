import os
import sqlite3
from datetime import datetime
import pytz
from tweepy import OAuthHandler

class App:
    """docstring for App."""
    def __init__(self, consumerKey, consumerSecret):
        self.auth = OAuthHandler(consumerKey, consumerSecret)

class User:
    """docstring for account."""
    def __init__(self, App, user, accessToken, accessSecret):
        self.App = App
        self.user = user
        self.auth = App.auth
        self.auth.set_access_token(accessToken, accessSecret)

class SQL:
    """docstring for SQL."""
    HOME=os.environ["HOME"]
    LOG_PATH="{HOME}/.twinfo/data.db".format(HOME=HOME)
    con=sqlite3.connect(LOG_PATH)
    c = con.cursor()

    @classmethod
    def __insert_notif(cls, event_notif):
        sql = "INSERT INTO notification VALUES (?, ?, ?, ?, ?, ?)"
        cls.con.execute(sql, event_notif)

    @classmethod
    def __insert_tweet(cls, event_tuple):
        # TODO すでに入っている場合
        sql = "INSERT OR IGNORE INTO tweet VALUES (?, ?, ?)"
        cls.con.execute(sql, event_tuple)

    @classmethod
    def insert_event(cls, event_tuple):
        cls.__insert_notif(event_tuple[0])
        cls.__insert_tweet(event_tuple[1])
        cls.con.commit()

def get_time(created_at):
    if type(created_at) is datetime:
        utctime=created_at
    else:
        utctime=datetime.strptime(created_at,"%a %b %d %H:%M:%S +0000 %Y")
    jptime=pytz.timezone('Asia/Tokyo').fromutc(utctime)
    time=jptime.strftime("%Y-%m-%d %H:%M:%S")
    time_var=jptime.strftime("%Y-%m-%d-%H%M%S")
    return time, time_var
