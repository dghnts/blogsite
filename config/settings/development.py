from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# summernoteで保存する画像の設定
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static"]