"""
Variables de entorno (mismo criterio que Cluster PGM / Lautaro Diesel).
Lee .env en desarrollo y variables de Railway en producción.
"""
import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="django-insecure-miryam-dev-key")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[]) if not DEBUG else ["*"]
if not DEBUG and os.environ.get("PORT") and not env.list("ALLOWED_HOSTS", default=[]):
    ALLOWED_HOSTS.append(".up.railway.app")

_raw_csrf_origins = env.list("CSRF_TRUSTED_ORIGINS", default=[])
CSRF_TRUSTED_ORIGINS = [
    o if o.startswith(("http://", "https://")) else f"https://{o}"
    for o in _raw_csrf_origins
    if (o and o.strip())
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DB_ENGINE = env("DB_ENGINE", default="sqlite3")
DB_USER = env("DB_USER", default="")
DB_PASSWORD = env("DB_PASSWORD", default="")
DB_HOST = env("DB_HOST", default="")
DB_PORT = env("DB_PORT", default="")
DB_NAME = env("DB_NAME", default="miryam")

CONTACT_FORM_RECIPIENT_EMAIL = env(
    "CONTACT_FORM_RECIPIENT_EMAIL",
    default="agusgattasrp@gmail.com",
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="web@miryambarovero.com.ar")

# EmailJS (misma cuenta que Stork Landing — envío desde el navegador)
EMAILJS_SERVICE_ID = env("EMAILJS_SERVICE_ID", default="service_392pf6s")
EMAILJS_TEMPLATE_ID = env("EMAILJS_TEMPLATE_ID", default="template_qhkfc1d")
EMAILJS_PUBLIC_KEY = env("EMAILJS_PUBLIC_KEY", default="uT_FIk0s12tcwpouj")

EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
