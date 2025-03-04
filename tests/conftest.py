import pytest
import logging

from app.app import create_app, db
from app.db.models import Roles, Languages

log_file = "logs/pytest.log"
log_format = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
log_level = logging.DEBUG
logging.basicConfig(
    filename=log_file,
    level=log_level,
    format=log_format,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        logger.error(f"Test {item.name} failed in function: {item.function.__name__}")
        logger.error(f"Captured stdout: {call.excinfo.value if call.excinfo else 'No exception info'}")

@pytest.fixture(scope="session")
def app():
    app = create_app("TEST")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="session")
def fill_db_with_roles(app):
    with app.app_context():
        roles = [Roles(id=1, role="admin"), Roles(id=2, role="user")]
        db.session.bulk_save_objects(roles)

        langs = [Languages(id=1, language="eng"), Languages(id=2, language="rus")]
        db.session.bulk_save_objects(langs)

        db.session.commit()
        yield
        db.session.rollback()

@pytest.fixture
def client(app, fill_db_with_roles):
    return app.test_client()


# @pytest.fixture(scope="session", autouse=True)
# def configure_logging():
#     log_file = "logs/pytest.log"
#     log_format = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
#     log_level = logging.DEBUG
#
#     for handler in logging.root.handlers[:]:
#         logging.root.removeHandler(handler)
#
#     logging.basicConfig(
#         filename=log_file,
#         level=log_level,
#         format=log_format,
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )
#
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)
#     console_handler.setFormatter(logging.Formatter(log_format))
#
#     logging.getLogger().addHandler(console_handler)
#
#     logging.info("Logging is set up!")

