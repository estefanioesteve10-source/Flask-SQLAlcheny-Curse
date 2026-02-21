#!/usr/bin/env bash
# Sair imediatamente se um comando falhar
#!/usr/bin/env bash
set -e

# Instala as dependências
pip install -r requirements.txt

# Roda as migrações (usando o caminho do seu app)
flask --app src.app db upgrade

# Inicia o Gunicorn apontando para o arquivo wsgi.py que criamos
gunicorn wsgi:app