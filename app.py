import logging
from flask import Flask
from credentials import Credentials
from db.models import create_tables
from extentions import jwt, db


credentials = Credentials()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(credentials.get("LOGFILE"))
    ]
)
logger = logging.getLogger(__name__)


def main():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = credentials.get("JWT_SECRET_KEY")
    jwt.init_app()

    db.init_app(app)

    create_tables(db)


if __name__ == "__main__":
    main()
