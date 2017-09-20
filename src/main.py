# -*- coding: utf-8 -*-

import yaml
import time
import sys

from util import App, User
from Streaming import Streaming

def get_users():
    YAML_PATH = 'conf/conf.yaml'
    with open(YAML_PATH, 'r') as f:
        data=yaml.load(f)
    app = App(**data['app'])
    users= [User(app, user, **setting) for user, setting in data['users'].items()]
    return users

def get_user(input_key):
    YAML_PATH = 'conf/conf.yaml'
    with open(YAML_PATH, 'r') as f:
        data=yaml.load(f)
    app = App(**data['app'])
    setting = data["users"][input_key]
    user= User(app, input_key, **setting)
    return user

def main():
    user = get_user(sys.argv[1])
    Streaming(user).start()
    # 並列うまくいかない
    # users = get_users()
    # joblib.Parallel(n_jobs=len(users)+1)(
    #     [joblib.delayed(start_streaming)(Streaming(user)) for user in users]
    # )


if __name__ == '__main__':
    main()
