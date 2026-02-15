from http import HTTPStatus

from flask import Blueprint, request

# importando recursos do app.py
from src.app import User, db

app = Blueprint('user', __name__, url_prefix='/users')

# criando usuario
def _create_user():
    data = request.json                          # pega os dados da requisição em json
    user = User(username=data['username'])       # pega o username da requisição
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
        }
        for user in users
    ]

@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        _create_user()
        return {'message': 'User created!'}, HTTPStatus.CREATED
    else:
        return {'users': _list_users() }