import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-dev-key-change-in-prod'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',

    # Local apps
    'core',
    'authentication',
    'rides',
    'notifications',
    'mobile_backend',
]

MIDDLEWARE = [
    'core.middleware.request_id.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mobile_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mobile_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exceptions.handler.custom_exception_handler',
}

# === OBSERVABILITY LOGGING - TASK 1 ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'structured': {
            'format': '[{asctime}] {levelname} [{name}] req_id=%(request_id)s | %(message)s',
            'style': '%',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'structured',
        },
        'file_app': {
            'class': 'logging.FileHandler',
            'filename': str(BASE_DIR / 'logs' / 'application.log'),
            'formatter': 'structured',
        },
    },
    'loggers': {
        'application': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'authentication': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'api': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'database': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'celery': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'websocket': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'security': {'handlers': ['console', 'file_app'], 'level': 'WARNING', 'propagate': False},
    },
}

# Celery
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
# Redis unte:
# 'BACKEND': 'django_redis.cache.RedisCache',
# 'LOCATION': 'redis://127.0.0.1:6379/1',
