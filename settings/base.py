import os
from flask import Flask


class BaseConfig(object):
    app = Flask(__name__)

    DB_URL = f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}" \
             f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SERVER_HOST = '127.0.0.1'
    SECRET_KEY = 'Lz176a9Vr18E4JobEZdkpoExE6VEhu0M'

    # DB SETTINGS

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
