import os
from flask import Flask


class BaseConfig(object):
    app = Flask(__name__)

    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SERVER_HOST = '127.0.0.1'
    DB_NAME = 'database.db'
    SECRET_KEY = 'Lz176a9Vr18E4JobEZdkpoExE6VEhu0M'

    # DB SETTINGS

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_HOST')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
