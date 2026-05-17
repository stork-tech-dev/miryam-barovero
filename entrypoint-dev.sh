#!/bin/bash
set -e

mkdir -p /code/media

echo "Ejecutando migraciones..."
python manage.py migrate

# shellcheck source=ensure_superuser.sh
source ./ensure_superuser.sh

echo "Iniciando servidor de desarrollo..."
exec python manage.py runserver 0.0.0.0:8000
