import os

# Flask
DEBUG = False

# local_config.pyファイルを読み込み
try:
    from .local_config import *
except ImportError:
    pass

if not DEBUG:
    # SECRET_KEY設定
    SECRET_KEY = os.environ['YOUR_CHANNEL_SECRET']

    # sqlalchemy設定
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
        'user': os.getenv('DB_USER', os.environ['DB_USERNAME']),
        'password': os.getenv('DB_PASSWORD', os.environ['DB_PASSWORD']),
        'host': os.getenv('DB_HOST', os.environ['DB_HOSTNAME']),
        'db': os.getenv('DB_NAME', os.environ['DB_NAME']),
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
