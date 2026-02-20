import pytest
from flask_jwt_extended import create_access_token

from src.app import create_app, db

@pytest.fixture()
def app():
    app = create_app(
        {
            "SECRET_KEY":'dev',
            "SQLALCHEMY_DATABASE_URI":'sqlite://',
            "JWT_SECRET_KEY" : "test",
        }
    )
    with app.app_context():
        db.create_all()
        # other setup can go here
        yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def admin_headers(client):
    # Lógica simplificada para retornar um header pronto
    token = create_access_token(identity="1") # ID de um admin fake
    return {"Authorization": f"Bearer {token}"}