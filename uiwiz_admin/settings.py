"""
Django settings for uiwiz-admin.
Uses the same database as uiwiz-backend (config.properties or env vars).
"""
import os
from pathlib import Path

from .config_reader import get_config

BASE_DIR = Path(__file__).resolve().parent.parent
config = get_config()

SECRET_KEY = config.get("django.secret_key", "admin-insecure-change-me")
DEBUG = config.get("django.debug", "True").lower() == "true"
ALLOWED_HOSTS = [
    h.strip() for h in config.get("django.allowed_hosts", "localhost,127.0.0.1").split(",")
]

ENCRYPTION_KEY = config.get("encryption.key", "")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "dashboard",
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

ROOT_URLCONF = "uiwiz_admin.urls"
WSGI_APPLICATION = "uiwiz_admin.wsgi.application"

# Same database as uiwiz-backend
DATABASES = {
    "default": {
        "ENGINE": config.get("db.engine", "django.db.backends.postgresql"),
        "NAME": config.get("db.name", "uiwiz"),
        "USER": config.get("db.user", ""),
        "PASSWORD": config.get("db.password", ""),
        "HOST": config.get("db.host", "localhost"),
        "PORT": config.get("db.port", "5432"),
        "OPTIONS": {
            "sslmode": config.get("db.sslmode", "require" if not DEBUG else "prefer"),
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom login (no Django admin pages)
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
