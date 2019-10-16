import os
from flask import Flask


class BaseConfig(object):
    app = Flask(__name__)

    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SERVER_HOST = '127.0.0.1'
    DB_NAME = 'database.db'
    SECRET_KEY = 'Lz176a9Vr18E4JobEZdkpoExE6VEhu0M'

    # DB SETTINGS

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/' + DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False
