#!/usr/bin/env bash
# Sair imediatamente se um comando falhar
set -e

# 1. Instalar as dependências do requirements.txt
pip install -r requirements.txt

# 2. Rodar as migrações do banco de dados (se você usa Flask-Migrate)
flask --app src.app db upgrade

# 3. Iniciar o servidor com Gunicorn
# Nota: Se o seu arquivo de entrada for src/app.py, use src.app:app
gunicorn src.app:app