from os import environ

from dotenv import load_dotenv

from application import create_app
from config import DevConfig
from config import ProductionConfig
from config import TestConfig

load_dotenv(dotenv_path='/Volumes/SANDISK/Python Projects/DVDLibrary/.env')
ENV = environ.get('ENV')

if ENV == 'development':
    app = create_app(DevConfig)
elif ENV == 'testing':
    app = create_app(TestConfig)
else:
    app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run(host='127.0.0.1')
