
from os import environ

from dotenv import load_dotenv

load_dotenv(dotenv_path='/Volumes/SANDISK/Python Projects/DVDLibrary/.env')


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or 'False'
    FLASK_ENV = environ.get('FLASK_ENV')
#    WTF_CSRF_ENABLED = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')



class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    TESTING = environ.get('TESTING')


class TestConfig(Config):
    TESTING = environ.get('TESTING')
    WTF_CSRF_ENABLED = environ.get('WTF_CSRF_ENABLED')
    TEST_DB = environ.get('TEST_DB')
    BASEDIR = environ.get('BASEDIR')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_TEST_DATABASE_URI')
