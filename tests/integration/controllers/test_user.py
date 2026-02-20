from http import HTTPStatus

from flask_jwt_extended import create_access_token

from src.app import User, db, Role

def test_get_user_sucess(client, admin_headers, user_return):
    # Given
    user = user_return

    # Where
    # 3. Fazer a requisição com o Header de autorização
    response = client.get(f"/users/{user.id}", headers=admin_headers)

    # Then
    assert  response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
        "role": user.role.name,  # Mudamos de dicionário para string
    }
    db.session.remove()


def test_get_user_not_found(client, admin_headers):

    user_id = 2

    # Where
    # 3. Fazer a requisição com o Header de autorização
    response = client.get(f"/users/{user_id}", headers=admin_headers)

    # Then
    assert  response.status_code == HTTPStatus.NOT_FOUND
    db.session.remove()


def test_list_users(client, admin_headers):

    query = db.select(User)
    users = db.session.execute(query).scalars().all()

    # Where
    # 3. Fazer a requisição com o Header de autorização
    response = client.get(f"/users/", headers=admin_headers)

    # Then
    assert  response.status_code == HTTPStatus.OK
    assert response.json == {
        'users':[
                    {
                        "id": user.id,
                        "username": user.username,
                        "role": {
                            "id": user.role_id,
                            "name": user.role.name,
                        }
                    }
                ]
        for user in users
        }
    db.session.remove()


def test_list_users_fail(client):

    # Where
    # 3. Fazer a requisição com o Header de autorização
    response = client.get(f"/users/")

    # Then
    assert  response.status_code == HTTPStatus.UNAUTHORIZED
    db.session.remove()


def test_create_user(client,admin_headers,user_return):
    # Given
    user = user_return
    create_user = {
        "username": "NovoUsuario",
        "password": "password123",
        "role_id": user.id
    }

    # Where
    # 3. Fazer a requisição com o Header de autorização
    response = client.post(f"/users/", headers=admin_headers, json=create_user)

    # Then
    assert  response.status_code == HTTPStatus.CREATED
    assert response.json == {'message': 'User created!'}
    db.session.remove()