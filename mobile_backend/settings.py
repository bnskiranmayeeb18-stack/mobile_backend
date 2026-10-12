from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-test-key-for-local-dev-only'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'rides',
    'notifications',

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.request_id.RequestIdMiddleware',
    'core.middleware.performance.PerformanceMiddleware',
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

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exceptions.handler.custom_exception_handler',
}

# CACHE - Redis optional, local memory fallback
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# CELERY
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# LOGGING - OBSERVABILITY
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'structured': {
            'format': '[{asctime}] [{levelname}] [{name}] [req:{request_id}] [user:{user_id}] {method} {endpoint} {status_code} {execution_time}ms - {message}',
            'style': '{',
        },
    },
    'filters': {
        'request_id': {
            '()': 'core.middleware.request_id.RequestIdFilter',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'structured',
        },
        'app_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'application.log'),
            'maxBytes': 10*1024*1024,
            'backupCount': 5,
            'filters': ['request_id'],
            'formatter': 'structured',
        },
        'api_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'api.log'),
            'maxBytes': 10*1024*1024,
            'backupCount': 5,
            'filters': ['request_id'],
            'formatter': 'structured',
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'security.log'),
            'maxBytes': 10*1024*1024,
            'backupCount': 5,
            'filters': ['request_id'],
            'formatter': 'structured',
        },
        'celery_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'celery.log'),
            'maxBytes': 10*1024*1024,
            'backupCount': 5,
            'filters': ['request_id'],
            'formatter': 'structured',
        },
    },
    'loggers': {
        'application': {'handlers': ['console','app_file'], 'level': 'INFO', 'propagate': False},
        'authentication': {'handlers': ['console','app_file','security_file'], 'level': 'INFO', 'propagate': False},
        'api': {'handlers': ['console','api_file'], 'level': 'INFO', 'propagate': False},
        'database': {'handlers': ['console','app_file'], 'level': 'INFO', 'propagate': False},
        'celery': {'handlers': ['console','celery_file'], 'level': 'INFO', 'propagate': False},
        'websocket': {'handlers': ['console','app_file'], 'level': 'INFO', 'propagate': False},
        'security': {'handlers': ['console','security_file'], 'level': 'WARNING', 'propagate': False},
        'django.request': {'handlers': ['console','api_file'], 'level': 'WARNING', 'propagate': False},
    }
}