import datetime

import click
import sqlalchemy as sa
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

#criando a tabela User
class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.Integer, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, username={self.username!r}'

#criando a tabela Post
class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r}'

#inicialização do banco de dados "flask --app app inti-db"
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')


# initialize the app with the extension
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///bank.db',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # registrar comando cli
    app.cli.add_command(init_db_command)
    # inicializar a extensão
    db.init_app(app)

    # registro do blueprints
    from src.controllers import user
    app.register_blueprint(user.app)
    from src.controllers import post
    app.register_blueprint(post.app)
    return app