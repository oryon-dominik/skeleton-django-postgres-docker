"""
Django base settings.
For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import environ
from pathlib import Path

# Build paths inside the project like this: ROOT_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / 'apps'

env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    dotenvpath = ROOT_DIR / ".envs" / ".production.env"
    if not dotenvpath.exists():
        raise ValueError("Production dotenv file does not exist (create .envs/.production.env)")
    env.read_env(str(dotenvpath))

#======PROJECT-SPECIFIC-SETTINGS===============================================
# add project specific CONSTANTS here
PROJECT_TITLE = "skeleton-django-postgres-docker-compose"
#==============================================================================

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT")
POSTGRES_OPTIONS = ""
POSTGRES_SSL = "require" if DEBUG else "allow"
DATABASE_URL = env.str("DATABASE_URL", default=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}{POSTGRES_OPTIONS}")
DATABASES = {"default": env.db("DATABASE_URL", default=DATABASE_URL)}
# sqlite:
# DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ROOT_DIR / 'database' / 'sqlite.db'}}
# DATABASES["default"]["ATOMIC_REQUESTS"] = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# APPS
# Application definition-------------------------------------------------------
# project specific apps
PROJECT_APPS = [
    "apps.things.apps.ThingsConfig",
]
# custom apps for all projects
LOCAL_APPS = [
    # custom apps
    "apps.users.apps.UsersConfig",

]
DJANGO_APPS = [
    # default django-apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [  # order is important!!
    "crispy_forms",
    "crispy_tailwind",
    "django_extensions",
    'widget_tweaks',
]
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
# local apps shall override djangos default, so order is important
INSTALLED_APPS = PROJECT_APPS + LOCAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS


# users
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/" # "users:redirect"
LOGOUT_REDIRECT_URL = "users:login"
# LOGIN_REDIRECT_URL = "/"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "users:login"

# Django Admin URL.
# a little protection to script-kiddie-attacks. This is no REAL security.
ADMIN_URL = env.str("DJANGO_ADMIN_URL", default="secretadmin-kwM1jSAD7/")

# crispy forms
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


MIDDLEWARE = [  # order is important: https://docs.djangoproject.com/en/dev/ref/middleware/#middleware-ordering
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [str(ROOT_DIR / "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.request"
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging

# The logging-filter 'log_database_queries' will log to the file, if LOG_DATABASE is True
# Turn it only on in develop
LOG_DATABASE = False

# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING_FILE_HANDLER = 'logging.FileHandler'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'log_database_queries': {
            '()': 'config.logfilters.LogDatabaseQueriesFilter',
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            'filters': ['require_debug_true'],
            "class": "logging.StreamHandler",
            "formatter": "simple" if DEBUG else "verbose",
        },
        'requests_file': {
            'level': 'INFO',
            'class': LOGGING_FILE_HANDLER,
            'filename': str(ROOT_DIR / "logs" / "requests.log"),
        },
        'database_queries_file': {
            'level': 'DEBUG',
            'filters': ['log_database_queries'],
            'class': LOGGING_FILE_HANDLER,
            'filename': str(ROOT_DIR / "logs" / "database_queries.log"),
        },
        'server_log_file': {
            'level': 'INFO',
            'class': LOGGING_FILE_HANDLER,
            'filename': str(ROOT_DIR / "logs" / "server.log"),
            "formatter": "verbose",
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', "server_log_file"],
            'level': 'INFO',
            'propagate': True,
            },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['database_queries_file'],
            'propagate': True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", 'server_log_file'],
            "propagate": False,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        "OPTIONS": {"min_length": 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# localization-----------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = "en-us"
# german localization: LANGUAGE_CODE = 'de-de'
TIME_ZONE = "UTC"
# german localization: TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# To use a CDN (e.g.: for whitenoise), SET a statichost, (preferably as env):
STATIC_HOST = ''
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = f"{STATIC_HOST}/assets/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(ROOT_DIR / "assets")]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "config.finders.AssetsAppDirectoriesFinder",
]
MEDIA_ROOT = str(ROOT_DIR / "media")
MEDIA_URL = f"{STATIC_HOST}/media/"
