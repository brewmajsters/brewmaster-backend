import os
from flask import Flask
from dotenv import load_dotenv


class BaseConfig(object):
    from pathlib import Path

    app = Flask(__name__)

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(PROJECT_ROOT)
    ENV_PATH = Path(PROJECT_ROOT) / '..' / '.env'

    load_dotenv(dotenv_path=ENV_PATH)

    DB_URL = f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}" \
             f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

    DEBUG = False
    TESTING = False
    FLASK_ENV = 'development'

    SERVER_HOST = os.getenv('SERVER_HOST')
    SERVER_PORT = os.getenv('SERVER_PORT')

    SECRET_KEY = 'Lz176a9Vr18E4JobEZdkpoExE6VEhu0M'

    # DB SETTINGS

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
