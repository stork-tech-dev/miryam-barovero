#!/bin/bash
set -e

mkdir -p /code/media

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# shellcheck source=ensure_superuser.sh
source ./ensure_superuser.sh

echo "Iniciando servidor..."
PORT="${PORT:-8000}"
exec gunicorn -w 2 -b "0.0.0.0:${PORT}" miryam_site.wsgi:application --timeout 120
