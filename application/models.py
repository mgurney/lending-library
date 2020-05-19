from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from application import db


class User(UserMixin, db.Model):
    #  Model for user accounts

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )
    rules_read = db.Column(db.Boolean, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    dvd = db.relationship("DVD", backref="dvd_owner_id", lazy="dynamic")
    magazine = db.relationship("Magazine", backref="mag_owner_id", lazy="dynamic")

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        print(password, self.password)
        print(check_password_hash(self.password, password))
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.name)


class DVD(db.Model):

    # Model for DVD-Library
    __tablename__ = "dvds"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner_name = db.Column(db.String(50))
    format_dvd = db.Column(db.Boolean, nullable=True, unique=False)
    format_bluray = db.Column(db.Boolean, nullable=True, unique=False)
    format_4k = db.Column(db.Boolean, nullable=True, unique=False)
    rating = db.Column(db.String(5), nullable=False, unique=False)
    borrower_id = db.Column(db.String(50), nullable=True, unique=False)
    borrower_name = db.Column(db.String(50), nullable=True, unique=False)
    date_borrowed = db.Column(db.DateTime, nullable=True, unique=False)


class Magazine(db.Model):

    # Model for Magazine Library
    __tablename__ = "magazines"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner_name = db.Column(db.String(50))
    borrower_id = db.Column(db.String(50), nullable=True, unique=False)
    borrower_name = db.Column(db.String(50), nullable=True, unique=False)
    date_borrowed = db.Column(db.DateTime, nullable=True, unique=False)
