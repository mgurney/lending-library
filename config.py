import os
from os import environ

from dotenv import load_dotenv

load_dotenv(dotenv_path='/Volumes/SANDISK/Python Projects/DVDLibrary/.env')


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or 'False'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    TESTING = True
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TEST_DB = 'test.db'
    BASEDIR = '/Volumes/SANDISK/Python Projects/DVDLibrary/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, TEST_DB)
