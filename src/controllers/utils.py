from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from src.app import User, db
from functools import wraps


def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            # Busca o usuário de forma segura
            user = db.session.get(User, user_id)

            if not user:
                return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED

            # Verifica a role
            if user.role.name != role_name:
                return {"message": f"Required role: {role_name}"}, HTTPStatus.FORBIDDEN

            return f(*args, **kwargs)
        return wrapped
    return decorator