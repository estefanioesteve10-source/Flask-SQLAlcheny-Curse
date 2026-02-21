import datetime
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from src.models.base import db
from flask_migrate import Migrate


migrate = Migrate()
jwt = JWTManager()


# initialize the app with the extension
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
        JWT_SECRET_KEY = "super-secret",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # inicializar a extensão
    db.init_app(app)
    # iniciando a migração
    migrate.init_app(app, db)
    # iniciando o jwt
    jwt.init_app(app)

    # registro do blueprints
    from src.controllers import user
    app.register_blueprint(user.app)
    from src.controllers import post
    app.register_blueprint(post.app)
    from src.controllers import auth
    app.register_blueprint(auth.app)
    from src.controllers import role
    app.register_blueprint(role.app)
    return app