import os
import subprocess
import sys
from pathlib import Path
import re
import socket

from corsheaders.defaults import default_headers
from graphql.type.definition import GraphQLEnumValue

from .mp import MonkeyPathingGraphQLEnumValue


def get_host_ip():
    """Определяет локальный IPv4 адрес хоста с безопасными fallback.
    - На Windows использует socket.gethostbyname.
    - На Linux/Alpine пробует `hostname -i` (поддерживается в busybox) и socket.
    - При любой ошибке возвращает 127.0.0.1, чтобы не падать при старте.
    """
    try:
        # Попытка 1: Windows — напрямую через socket
        if sys.platform.startswith("win"):
            ip = socket.gethostbyname(socket.gethostname())
            if re.match(r"^(\d+\.){3}\d+$", ip):
                return ip
            return "127.0.0.1"

        # Попытка 2: Linux/Alpine — hostname -i (а не -I), затем парсим IPv4
        try:
            output = subprocess.check_output(["hostname", "-i"], stderr=subprocess.DEVNULL)
            for address in output.decode().strip().split():
                if re.match(r"^(\d+\.){3}\d+$", address):
                    return address
        except Exception:
            pass

        # Попытка 3: generic socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if re.match(r"^(\d+\.){3}\d+$", ip):
                return ip
        finally:
            s.close()
    except Exception:
        pass
    return "127.0.0.1"


DEV = os.environ.get("DEV", "not") == "true"
DEBUG = bool(os.environ.get("DEBUG", False))
SECRET_KEY = os.environ.get("SECRET_KEY")
TG_KEY = os.environ.get("TG_KEY")

### MINIO
MINIO_SERVER = os.environ.get("MINIO_SERVER") or get_host_ip()
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
MINIO_BUCKET = os.environ.get("MINIO_BUCKET")
MINIO_PREFIX = f"{os.environ.get('MINIO_PREFIX', '')}/{MINIO_BUCKET}"
#############

# CELERY and REDIS
CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_RESULT_EXTENDED = True
#############

### Сертификаты для TLS
RUSSIAN_TRUST = "core/certs/min_cifr.pem"
#############

# JUMP_FINANCE
JUMP_FINANCE_CLIENT_KEY = os.environ.get("JUMP_FINANCE_CLIENT_KEY")
JF_AGENT_ID = os.environ.get("JUMP_FINANCE_AGENT_ID")
JUMP_FINANCE_ROOT_ENDPOINT = os.environ.get("JUMP_FINANCE_ROOT_ENDPOINT")
#############

# FIREBASE
FIREBASE_SERVER_KEY = os.environ.get("FIREBASE_SERVER_KEY")
FIREBASE_URL_SERVER = os.environ.get("FIREBASE_URL_SERVER")
FCM_TITLE = os.environ.get("FIREBASE_TITLE")
#############

# TBANK
TINKOFF_PAYMENT_URL = os.environ.get("TINKOFF_PAYMENT_URL")
TINKOFF_PAYMENT_CANCEL_URL = os.environ.get("TINKOFF_PAYMENT_CANCEL_URL")
TERMINAL_KEY = os.environ.get("TINKOFF_TERMINAL_KEY")
PASSWORD_TERMINAL = os.environ.get("TINKOFF_PASSWORD_TERMINAL")
#############

ASGI_APPLICATION = "core.asgi.application"
REST_FRAMEWORK = {"DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata"}
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = [".hoopsservice.ru", ".localhost:8020", "chrome-extension://kjhjcgclphafojaeeickcokfbhlegecd"]


GRAPHENE = {"SCHEMA": "core.schema.schema"}

INSTALLED_APPS = [
    "corsheaders",
    "graphene_django",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "django_celery_results",
    # "graphene_subscriptions",
    "payment",
    "otp",
    "hotels",
    "users",
    "executor",
    "manager",
    "settings",
    "closing_documents",
    "passports",
]

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": BASE_DIR / "backup"}

CRONJOBS = [("*/5 * * * *", "core.cron.backup_data")]

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    "Bearer",
]
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS_KEY", "").split(",")
CSRF_TRUSTED_ORIGINS.append("https://*.hoopsservice.ru")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRES_NAME"),
#         "USER": os.environ.get("POSTGRES_USER"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#         "HOST": "db",
#         "PORT": 5432,
#     },
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("MYSQL_DATABASE", "hoops"),
        "USER": os.environ.get("MYSQL_USER", "hoops"),
        "PASSWORD": os.environ.get("MYSQL_PASSWORD", "hoops"),
        "HOST": os.environ.get("MYSQL_HOST", "db_mysql"),
        "PORT": int(os.environ.get("MYSQL_PORT", 3306)),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

if "test" in sys.argv:
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"
    DATABASES["default"]["NAME"] = ":memory:"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "Ru-ru"

TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_ROOT = os.path.join(BASE_DIR, "data/")  # 'data' is my media folder
MEDIA_URL = "/media/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

GraphQLEnumValue.__init__ = MonkeyPathingGraphQLEnumValue.__init__

# import django
# django.setup()
