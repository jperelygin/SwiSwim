from flask import Flask
from endpoints.auth import auth_bp


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp)
