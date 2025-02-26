from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from credentials import Credentials


credentials = Credentials()

jwt = JWTManager()

db = SQLAlchemy()
