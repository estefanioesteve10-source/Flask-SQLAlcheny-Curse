from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import inspect

# importando recursos do app.py
from src.app import User, db
from src.controllers.utils import requires_role

app = Blueprint('user', __name__, url_prefix='/users')

# criando usuario
def _create_user():
    data = request.json                          # pega os dados da requisição em json
    user = User(
        username=data['username'],
        password=data['password'],
        role_id=data['role_id'],
    )       # pega o username da requisição
    db.session.add(user)                         # escrevendo o user no db
    db.session.commit()

# Listando os usuarios
def _list_users():
    # users = db.session.execute(db.select(User)).scalars().all()
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role_id,
                "name": user.role.name,
            }
        }
        for user in users
    ]

@app.route('/', methods=['GET', 'POST'])
@jwt_required() # proteger para pessoas autenticadas
@requires_role('admin')
def list_or_create_user():
    if request.method == 'POST':
        _create_user()
        return {'message': 'User created!'}, HTTPStatus.CREATED
    else:
        return {'users': _list_users() }

@app.route("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    # Pega o ID do usuário que está fazendo a requisição (do Token)
    current_user_id = int(get_jwt_identity())

    # Busca o objeto do usuário logado para verificar a Role
    current_user = db.session.get(User, current_user_id)

    # Lógica de permissão:
    # Só permite se: (O ID logado == ID da URL) OU (O usuário logado for Admin)
    if current_user_id != user_id and current_user.role.name != 'admin':
        return {"message": "Access denied. You can only see your own profile."}, HTTPStatus.FORBIDDEN

    # Se passou no teste, busca os dados do ID solicitado
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role.name
    }

@app.route("/<int:user_id>", methods=["PATCH"])
@jwt_required() # proteger para pessoas autenticadas
@requires_role('admin')
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    # o inspect para ver quais colunas existem no modelo User
    mapper = inspect(User)
    for column in mapper.attrs:
        # Impede que o ID seja alterado via PATCH
        if column.key in data and column.key != "id":
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }

@app.route("/<int:user_id>", methods=["DELETE"])
@jwt_required() # proteger para pessoas autenticadas
@requires_role('admin')
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT