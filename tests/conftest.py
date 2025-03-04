import pytest

from app.app import create_app, db
from app.db.models import Roles, Languages


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
