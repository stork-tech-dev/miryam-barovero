#!/bin/bash
# Crea o actualiza el superusuario si CREATE_SUPERUSER=true (Docker / Railway).
if [ "$CREATE_SUPERUSER" != "true" ] || [ -z "$SUPERUSER_USERNAME" ]; then
  return 0 2>/dev/null || exit 0
fi

SUPERUSER_EMAIL="${SUPERUSER_EMAIL:-admin@example.com}"
echo "Verificando superusuario..."
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('SUPERUSER_EXISTS' if User.objects.filter(username='$SUPERUSER_USERNAME').exists() else 'SUPERUSER_NOT_EXISTS')" | grep -q "SUPERUSER_EXISTS"; then
  echo "Superusuario ya existe, se actualizará..."
else
  echo "Superusuario no existe, se creará..."
fi

if [ -n "$SUPERUSER_PASSWORD" ]; then
  PASSWORD="$SUPERUSER_PASSWORD"
  echo "Usando contraseña de variable de entorno"
else
  PASSWORD=$(python -c "import secrets; import string; print(''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%^&*') for _ in range(12)))")
  echo "Generando contraseña aleatoria"
fi

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    user = User.objects.get(username='$SUPERUSER_USERNAME')
except User.DoesNotExist:
    user = User.objects.create_superuser(
        username='$SUPERUSER_USERNAME',
        email='$SUPERUSER_EMAIL',
        password='$PASSWORD'
    )
    print('Superusuario creado correctamente')
else:
    user.set_password('$PASSWORD')
    user.is_staff = True
    user.is_superuser = True
    user.email = '$SUPERUSER_EMAIL'
    user.save()
    print('Contraseña y configuración actualizadas correctamente')
"
echo "=========================================="
echo "SUPERUSUARIO CREADO/ACTUALIZADO:"
echo "Usuario: $SUPERUSER_USERNAME"
echo "Email: $SUPERUSER_EMAIL"
echo "Contraseña: $PASSWORD"
echo "=========================================="
