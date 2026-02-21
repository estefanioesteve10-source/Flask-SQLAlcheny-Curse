

import pytest
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.models.role import Role
from src.app import create_app, db


@pytest.fixture()
def app():
    app = create_app( environment="testing" )
    with app.app_context():
        db.create_all()
        # other setup can go here
        yield app
        db.session.remove() # Resolve o ResourceWarning de conexões abertas
        db.drop_all()       # Garante que o banco seja limpo para o próximo teste
        db.engine.dispose()

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def admin_headers(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username = "Vanda2", password = "123456", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    # Lógica simplificada para retornar um header pronto
    token = create_access_token(identity="1") # ID de um admin fake
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_return(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="Vanda5", password="123456", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    db.session.refresh(user) # Garante que o objeto tenha os dados atualizados do banco
    return user # <--- Retorne o objeto, assim user.id funcionará
