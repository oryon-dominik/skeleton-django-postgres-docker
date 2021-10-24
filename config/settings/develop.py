"""
Local Development settings
    * Debug is True
    * Any allowed hosts
"""

from .base import *  # NOSONAR, noqa

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", True)  # ! in development only!

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0KhFyew7z5nrJWYCSJXB_E_eaf6KwDoF715l66sfNH"

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# cors-headers are allowed for development
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:9000", # Vue Vite
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    # de-actived methods:
    # 'DELETE',
    # 'OPTIONS',
    # 'PATCH',
    # 'PUT',
]

# The logging-filter 'log_database_queries' will log to the file, if LOG_DATABASE is True
# Turn it only on in develop
LOG_DATABASE = False

# Django Admin URL.
ADMIN_URL = env.str("DJANGO_ADMIN_URL", default="admin/")

# for development emails are send to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# alternatively, deactivate email-verification with ACCOUNT_EMAIL_VERIFICATION = 'none'

IPYTHON_ARGUMENTS = ["--debug", "--settings=config.settings.develop"]
NOTEBOOK_ARGUMENTS = [  # to run the notebook with django 3 async set env DJANGO_ALLOW_ASYNC_UNSAFE=true
    "--port", "8888",  # -> set in docker-compose.yml
    "--ip", "0.0.0.0",
    "--allow-root",
    "--notebook-dir", "notebooks",
    "--no-browser"
    ]


# django-extensions------------------------------------------------------------
# debug-toolbar
def show_toolbar(request):
    return False #True

if DEBUG:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE.insert(4, "debug_toolbar.middleware.DebugToolbarMiddleware")
    # trick to have debug toolbar when developing with docker
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }
