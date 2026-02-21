import datetime
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from src.models.base import db
from flask_migrate import Migrate


migrate = Migrate()
jwt = JWTManager()


# initialize the app with the extension
def create_app(environment = os.environ['ENVIRONMENT']):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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