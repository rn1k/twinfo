import joblib
import yaml
import time
from Streaming import App, User, Streaming

def start_stream(Stream):
    Stream.start()

def get_users():
    import pprint
    YAML_PATH = 'src/conf/conf.yaml'
    with open(YAML_PATH, 'r') as f:
        data=yaml.load(f)
    app = App(**data['app'])
    settings = [setting for user, setting in data['users'].items()]
    users= [User(app, **setting) for setting in settings]
    return users

def main():

    users = get_users()
    joblib.Parallel(n_jobs=len(users))(
        [joblib.delayed(start_stream)(Streaming(user)) for user in users]
    )


if __name__ == '__main__':
    main()
