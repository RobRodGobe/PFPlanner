import pytest
from Backend.app import create_app
from Backend.extensions import db
from Backend.models import User


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user(app):
    with app.app_context():
        u = User(email="test@example.com", role="user")
        u.set_password("password")
        db.session.add(u)
        db.session.commit()
        return u
