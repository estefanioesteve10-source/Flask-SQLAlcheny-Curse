from http import HTTPStatus
from wsgiref import headers

from flask_jwt_extended import create_access_token
from pytest_mock import mocker

from src.app import User, db, Role

def test_get_user_sucess(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username = "Vanda", password = "123456", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # 2. Gerar o Token para o usuário criado
    # Certifica de que o identity aqui é o que o app espera (ID ou username)
    access_token = create_access_token(identity=str(user.id))
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Where
    # 3. Fazer a requisição com o Header de autorização
    response = client.get(f"/users/{user.id}", headers=headers)

    # Then
    assert  response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
        "role": user.role.name,  # Mudamos de dicionário para string
    }


def test_get_user_not_found(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="Temp", password="123", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    user_id = 2

    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    # Where
    # 3. Fazer a requisição com o Header de autorização
    response = client.get(f"/users/{user_id}", headers=headers)

    # Then
    assert  response.status_code == HTTPStatus.NOT_FOUND
