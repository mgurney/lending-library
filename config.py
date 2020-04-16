from os import environ

class Config:

    TESTING = environ.get('TESTING') or 'True'
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY') or 'jdaoiwehr.anb;sioudtj;aklj '

    #Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://dvd_library:Ng3^knLO!c59Cuo*3*u&@192.168.0.2/dvd_library'
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or 'False'
