import os
from flask import Flask
from dotenv import load_dotenv


class BaseConfig(object):
    from pathlib import Path

    app = Flask(__name__)
    env_path = Path('.') / '.env'

    load_dotenv(dotenv_path=env_path)

    DB_URL = f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}" \
             f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

    DEBUG = False
    TESTING = False
    FLASK_ENV = 'development'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SERVER_HOST = os.getenv('SERVER_HOST')
    SERVER_PORT = os.getenv('SERVER_PORT')

    SECRET_KEY = 'Lz176a9Vr18E4JobEZdkpoExE6VEhu0M'

    # DB SETTINGS

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
