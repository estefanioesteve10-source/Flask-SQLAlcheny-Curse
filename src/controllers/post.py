from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import inspect

# importando recursos do app.py
from src.app import db
from src.models.post import Post

app = Blueprint('post', __name__, url_prefix='/posts')

# criando usuario
def _create_post():
    data = request.json                          # pega os dados da requisição em json
    post = Post(
        title=data.get('title'),
        body=data.get('body'),
        author_id=data.get('author_id')
    )
    db.session.add(post)
    db.session.commit()

# Listando os usuarios
def _list_posts():
    # posts = db.session.execute(db.select(User)).scalars().all()
    query = db.select(Post)
    posts = db.session.execute(query).scalars().all()
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "created": post.created,
            "author_id": post.author_id,
        }
        for post in posts
    ]

@app.route('/', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'POST':
        _create_post()
        return {'message': 'Post created!'}, HTTPStatus.CREATED
    else:
        return {'posts': _list_posts() }

@app.route("/<int:post_id>")
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id,
    }

@app.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    # o inspect para ver quais colunas existem no modelo User
    mapper = inspect(Post)
    for column in mapper.attrs:
        # Impede que o ID seja alterado via PATCH
        if column.key in data and column.key != "id":
            setattr(post, column.key, data[column.key])

    db.session.commit()

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "author_id": post.author_id,
        "created": str(post.created)  # Converte a data para string simples
    }

@app.route("/<int:post_id>", methods=["DELETE"])
def delete_user(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT