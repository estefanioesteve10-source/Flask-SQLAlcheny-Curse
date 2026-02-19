from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import inspect

# importando recursos do app.py
from src.app import User, db, Role

app = Blueprint('role', __name__, url_prefix='/roles')

@app.route('/', methods=['POST'])
def create_role():
    data = request.json
    role = Role(name=data['name'])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created"}, HTTPStatus.CREATED
