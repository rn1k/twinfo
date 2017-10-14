# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import Stream

import traceback
import pprint
pp = pprint.PrettyPrinter(indent=4)

from util import SQL, get_time

class EventManager:
    """docstring for EventManager"""

    # クラス変数
    EVENT_DIC = {}

    def __init__(self, user, status):
        self.status = status
        self.user = user
        self.time, self.time_var = get_time(status.created_at)
        # event
        self.event = status.event
        self.src_screen_name = status.source['screen_name']
        self.src_name = status.source['name']
        self.src_uid = status.source['id_str']
        self.src_icon = status.source['profile_image_url'].replace('_normal', '')
        # 出力
        output = {"event": self.event, "name": self.src_screen_name, "time": self.time}
        event = "{event} by @{name} ({time})".format(**output)
        print(event)
        # target
        self.trg_screen_name = status.target["screen_name"]
        self.trg_name = status.target['name']
        self.trg_uid = status.target["id_str"]
        self.trg_icon = status.target['profile_image_url'].replace('_normal', '')
        if status.event in ["favorite","unfavorite"]:
            self.trg_id = status.target_object['id_str']
            tmp = get_time(status.target_object['created_at'])
            self.trg_time, self.trg_time_var = tmp
            self.trg_text = status.target_object['text']
            self.has_media = ("media" in status.target_object["entities"])
            # 出力
            output = { "name": self.trg_screen_name,
                       "text": self.trg_text,
                       "time": self.trg_time }
            target = "@{name}: {text} ({time})".format(**output)
            print(target)
        else:
            self.trg_id = None
            self.trg_time, self.trg_time_var = None, None
            self.trg_text = None


    def __get_event_tuple(self):
        # 通し番号
        if (self.event not in self.EVENT_DIC):
            self.EVENT_DIC[self.event] = len(self.EVENT_DIC)

        event_notif= ( None,
                    self.src_uid,
                    self.EVENT_DIC[self.event],
                    self.trg_uid,
                    self.trg_id,
                    self.time )
        event_tweet = ( self.trg_id,
                        self.trg_text,
                        self.trg_time )
        event_src_user = ( self.src_uid,
                           self.src_screen_name,
                           self.src_name,
                           self.src_icon )
        event_trg_user = ( self.trg_uid,
                           self.trg_screen_name,
                           self.trg_name,
                           self.trg_icon )
        return (event_notif, event_tweet, event_src_user, event_trg_user)

    def insert_event(self):
        event_tuple=self.__get_event_tuple()
        # print(data)
        SQL.insert_event(event_tuple)


class EventListner(StreamListener):

    def __init__(self, user):
        super(EventListner, self).__init__()
        self.user = user

    def on_delete(self, status_id, user_id):
        twid=str(status_id)
        uid=str(user_id)
        # print(twid, uid)
        # SQL.delete_tweet(twid,uid)

    def on_status(self, status):
        """userstreamで流れてくるデータの処理"""
        pass

    def on_event(self, status):
        em = EventManager(self.user, status)
        em.insert_event()

    def on_error(self, status):
        print("error")
        pp.pprint(status)
        self.wait()

    def wait(self):
        pass


class Streaming:
    """各アカウントでのストリーミング処理"""

    def __init__(self, User):
        self.user = User.user
        self.auth = User.auth

    def start(self):
        el = EventListner(self.user)
        while 1:
            try:
                stream = Stream(self.auth, el)
                print('start @{} '.format(self.user))
                stream.userstream()
                # stream.userstream(replies="all")
            except Exception as e:
                print('stop @{} '.format(self.user))
                print(traceback.format_exc())
                self.wait()

    def wait(self):
        pass

if __name__ == '__main__':
    Streaming(user).start()
