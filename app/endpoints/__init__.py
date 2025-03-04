from flask import Flask
from app.endpoints.auth import auth_bp


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp)
