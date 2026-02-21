from http import HTTPStatus

from flask import Blueprint, request

# importando recursos do app.py
from src.models.base import db
from src.models.role import Role

app = Blueprint('role', __name__, url_prefix='/roles')

@app.route('/', methods=['POST'])
def create_role():
    data = request.json
    role = Role(name=data['name'])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created"}, HTTPStatus.CREATED
