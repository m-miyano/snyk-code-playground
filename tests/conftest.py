import pytest

from app import create_app, db
from config import Config


class TestConfig(Config):
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True


@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
