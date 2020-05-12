import pymysql
from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
babel = Babel()


def create_app(config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)
    app.static_folder = "static"
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)

    with app.app_context():
        from application import library
        from application import users
        from application import models
        from application import functions

        # Create tables for our models
        db.create_all()

        return app
