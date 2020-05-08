import pymysql
from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    app.static_folder = "static"
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    babel = Babel(app)

    with app.app_context():
        from application import library
        from application import users
        from application import models

        # Create tables for our models
        db.create_all()

        return app
