import logging
from flask import Flask

from app.credentials import Credentials
from app.endpoints.auth import auth_bp
from app.extentions import db, jwt


logger = logging.getLogger(__name__)


def create_app(config_name=None):

    credentials = Credentials(config_name=config_name)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(credentials.get("LOGFILE"))
        ]
    )

    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = credentials.get("JWT_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = credentials.get("DB_URI")

    jwt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
