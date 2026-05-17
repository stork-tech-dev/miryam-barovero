import os
from pathlib import Path

from miryam_site.environment_variables import (
    BASE_DIR,
    CSRF_TRUSTED_ORIGINS,
    DEBUG,
    SECRET_KEY,
    ALLOWED_HOSTS,
    SECURE_PROXY_SSL_HEADER,
    DB_ENGINE,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    CONTACT_FORM_RECIPIENT_EMAIL,
    DEFAULT_FROM_EMAIL,
    EMAILJS_SERVICE_ID,
    EMAILJS_TEMPLATE_ID,
    EMAILJS_PUBLIC_KEY,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_USE_TLS,
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "content",
    "web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "miryam_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "web.context_processors.site_links",
                "web.context_processors.emailjs",
            ],
        },
    },
]

WSGI_APPLICATION = "miryam_site.wsgi.application"
ASGI_APPLICATION = "miryam_site.asgi.application"

if os.environ.get("DATABASE_URL"):
    import dj_database_url

    DATABASES = {"default": dj_database_url.parse(os.environ["DATABASE_URL"])}
elif DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME or "miryam",
            "USER": DB_USER or "miryam",
            "PASSWORD": DB_PASSWORD or "miryam",
            "HOST": DB_HOST or "localhost",
            "PORT": DB_PORT or "5432",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Cordoba"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static_assets",
]

MEDIA_URL = "/media/"
if os.environ.get("MEDIA_ROOT"):
    MEDIA_ROOT = Path(os.environ["MEDIA_ROOT"])
elif os.environ.get("RAILWAY_VOLUME_MOUNT_PATH"):
    MEDIA_ROOT = Path(os.environ["RAILWAY_VOLUME_MOUNT_PATH"])
else:
    MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SOCIAL_INSTAGRAM_URL = (
    "https://www.instagram.com/miryam_psi?igsh=MXcyaTdxZGV3M2gwcQ%3D%3D"
)
SOCIAL_FACEBOOK_URL = "https://www.facebook.com/miryam.barovero?locale=es_LA"
SOCIAL_WHATSAPP_URL = "https://wa.me/5493512467943"
SOCIAL_BLOG_URL = (
    "https://www.threads.com/@miryam_psi"
    "?xmt=AQG0fVcaMfUWEwngLOJGQwEHAtBhXP279Nl-56P-aqKs26g"
)

CONTACT_FORM_RECIPIENT_EMAIL = CONTACT_FORM_RECIPIENT_EMAIL
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
EMAILJS_SERVICE_ID = EMAILJS_SERVICE_ID
EMAILJS_TEMPLATE_ID = EMAILJS_TEMPLATE_ID
EMAILJS_PUBLIC_KEY = EMAILJS_PUBLIC_KEY

if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = EMAIL_PORT
    EMAIL_HOST_USER = EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = EMAIL_USE_TLS
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/panel/"
LOGOUT_REDIRECT_URL = "/"

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
