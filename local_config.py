import os

DEBUG = True

SECRET_KEY = 'SECRET_KEY'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/DB名?charset=utf8'.format(**{
    'user': os.getenv('DB_USER', 'ユーザー'),
    'password': os.getenv('DB_PASSWORD', 'パスワード'),
    'host': os.getenv('DB_HOST', 'localhost'),
})
