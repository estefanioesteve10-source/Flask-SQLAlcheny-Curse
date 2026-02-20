import pytest
from src.app import create_app

@pytest.fixture()
def app():
    app = create_app(
        {
            "SECRET_KEY":'dev',
            "SQLALCHEMY_DATABASE_URI":'sqlite://',
            "JWT_SECRET_KEY" : "test",
        }
    )
    # other setup can go here
    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()
