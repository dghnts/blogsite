from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib import messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p3*glay1+r$l2e!_q!6=hs@a10lvu2wvh!isxrsq0=f4^#*rkg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    "users.apps.UsersConfig",
    "django_summernote",
    "blog.templatetags.param_change",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
]

# DEBUGがTrueのとき、メールの内容は全て端末に表示させる
DEFAULT_FROM_EMAIL = "example@example.com"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    SENDGRID_API_KEY = "ここにsendgridのAPIkeyを記述する"  # 環境変数でも可
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTH_USER_MODEL = "users.CustomUser"
ACCOUNT_FORMS = {"signup": "users.forms.SignupForm"}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
#    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "config.urls"

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
                "blog.custom_context.categories_and_tags",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# summernoteで保存する画像の設定
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# summernoteの設定(エディタのサイズ調整)
# https://github.com/summernote/django-summernote
SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",
        "height": "480",
    }
}

# 許可するHTMLタグと属性の指定(XSSに注意。scriptタグとonclick,onsubmitなどの属性は追加厳禁)
# bleachで判定する
ALLOWED_TAGS = [
    "a",
    "div",
    "p",
    "span",
    "img",
    "em",
    "i",
    "li",
    "ol",
    "ul",
    "strong",
    "br",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "table",
    "tbody",
    "thead",
    "tr",
    "td",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "strike",
    "u",
    "sup",
    "sub",
    "font",
]

ATTRIBUTES = {
    "*": ["style", "align", "title", "style"],
    "a": [
        "href",
    ],
    "img": [
        "src",
    ],
}

REASONS = [
    ("記事の内容が不適切である", "内容が不適切"),
    ("虚偽の内容が含まれている", "虚偽の内容"),
    ("タグの乱用をしている", "タグの乱用"),
    ("プライバシーを侵害する内容である", "プライバシー"),
]

load_dotenv()

# socialacountログイン関連
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_OAUTH2_SECRET")

AUTHENTICATION_BACKENDS = (
    "social_core.backends.open_id.OpenIdAuth",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.twitter.TwitterOAuth",
    "django.contrib.auth.backends.ModelBackend",
    "django.contrib.auth.backends.ModelBackend",
)
