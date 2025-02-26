import logging
from extentions import db


logger = logging.getLogger(__name__)


class Roles(db.Model):
    __tablename__ = "Roles"
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    role = db.Column(db.String, nullable=False)


class Languages(db.Model):
    __tablename__ = "Languages"
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    language = db.Column(db.String, nullable=False)


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role_id = db.Column(db.SmallInteger, db.ForeignKey("Roles.id"))
    role = db.relationship("Roles")
    language_id = db.Column(db.SmallInteger, db.ForeignKey("Languages.id"))
    language = db.relationship("Languages")


class Routines(db.Model):
    pass


class Statistics(db.Model):
    pass


def create_tables(database):
    try:
        db.Model.metadata.create_all(database)
        logger.info(f"All tables are successfully created!")
    except Exception as e:
        logger.error(f"Tables are not created in database: {e}")
