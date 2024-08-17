from base import *
from pathlib import Path
import os

DEBUG = False

# ここにメール送信設定を入力する(Sendgridを使用する場合)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

DEFAULT_FROM_EMAIL = "example@example.com"

ALLOWED_HOSTS = ["std-blogsite.com"]

CSRF_TRUSTED_ORIGINS = ["https://std-blogsite.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["POSTGRESQL_DB_NAME"],
        "USER": os.environ["POSTGRESQL_DB_USER"],
        "PASSWORD": os.environ["POSTGRESQL_DB_PASS"],
        "HOST": "localhost",
        "PORT": "",
    }
}

STATIC_ROOT = "/var/www/{}/static".format(BASE_DIR.name)

# 下記はファイルのアップロード機能を有する場合のみ
MEDIA_ROOT = "/var/www/{}/media".format(BASE_DIR.name)
