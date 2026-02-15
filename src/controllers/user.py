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

@app.route('/', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        _create_user()
        return {'message': 'User created!'}, HTTPStatus.CREATED
    else:
        return {'users': [] }