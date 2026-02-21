#!/usr/bin/env bash
# Sair imediatamente se um comando falhar
set -e

poetry run flask --app src.app db upgrad

poetry run  gunicorn src.wsgi:app